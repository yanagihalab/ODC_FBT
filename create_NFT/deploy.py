from web3 import Web3
import json

# Alchemyのエンドポイント
ALCHEMY_URL = "https://polygon-amoy.g.alchemy.com/v2/bEUKpCtZTnk62AzONay8nfL9vN4jcjjX"

# ウォレット情報
PRIVATE_KEY = "0b4df868a1b28fe02836d06c35f8424f1812a8ffeae7ef999ae14a7162365b13"
MY_ADDRESS = "0x4E201833d980D6d022fFca4Fabcb4Fe9a1e31917"

# Web3インスタンスの作成
web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# ABIとバイトコードの読み込み
with open("MyNFT_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

with open("MyNFT_bytecode.txt", "r") as bytecode_file:
    contract_bytecode = bytecode_file.read()

# コントラクトのデプロイ関数
def deploy_contract():
    contract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    
    # トランザクション作成
    tx = contract.constructor().buildTransaction({
        'from': MY_ADDRESS,
        'nonce': web3.eth.get_transaction_count(MY_ADDRESS),
        'gas': 5000000,
        'gasPrice': web3.to_wei('30', 'gwei'),
    })
    
    # トランザクション署名
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    
    # トランザクション送信
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Deploying contract... TX Hash: {tx_hash.hex()}")
    
    # トランザクション結果を待機
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Contract deployed at address: {tx_receipt.contractAddress}")
    return tx_receipt.contractAddress

# コントラクトをデプロイ
contract_address = deploy_contract()
