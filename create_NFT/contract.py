import os
from logging import getLogger, INFO, basicConfig
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solcx import compile_source, set_solc_binary, install_solc

# 必要に応じてSolidityコンパイラをインストール
install_solc('0.8.22')

# `solc` のパスを指定
set_solc_binary('/home/admin-y/.solcx/solc-v0.8.22')

basicConfig(level=INFO)
logger = getLogger(__name__)

if __name__ == "__main__":
    load_dotenv()

    # 環境変数から設定を取得
    INFURA_URL = os.getenv("INFURA_URL")
    WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not INFURA_URL or not WALLET_ADDRESS or not SECRET_KEY:
        raise ValueError("Missing required environment variables.")

    # Web3インスタンスを作成
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    wallet_address = w3.toChecksumAddress(WALLET_ADDRESS)
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # コントラクトの読み込みとコンパイル
    with open("contract.sol", "r") as file:
        source = file.read()
        install_solc("0.8.22")
        compiled_sol = compile_source(
            source,
            output_values=["abi", "bin"]  # 必要な出力を指定
            )

    # コントラクトデータの抽出
    contract_id = next(iter(compiled_sol))
    contract_interface = compiled_sol[contract_id]

    # トランザクション設定
    base_tx = {
        "nonce": w3.eth.get_transaction_count(wallet_address),
        "gas": 1000000,
        "gasPrice": w3.eth.gas_price,  # 動的にガス代を取得
    }

    # コントラクトの作成
    contract = w3.eth.contract(
        abi=contract_interface["abi"], bytecode=contract_interface["bin"]
    )
    contract_tx = contract.constructor().buildTransaction(base_tx)

    # トランザクション署名
    signed_tx = w3.eth.account.sign_transaction(contract_tx, private_key=SECRET_KEY)

    # トランザクション送信
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.info(f"Transaction hash: {tx_hash.hex()}")

    # トランザクションの結果確認
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt["status"] == 1:
        logger.info("Transaction successful!")
        contract_address = receipt["contractAddress"]
        logger.info(f"Contract deployed at address: {contract_address}")
    else:
        logger.error("Transaction failed.")
