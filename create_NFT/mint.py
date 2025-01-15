from web3 import Web3
from eth_account import Account
import json

# 必要な情報
node_url = "https://polygon-amoy.g.alchemy.com/v2/Z_HZ6k3vLbqJom0WbQym1U3yHO-T34Lh"  # InfuraなどのEthereumノード
contract_address = "0x56D8CB8824CAA15E76206276A5108DE0E7386D77"  # デプロイ済みのコントラクトアドレス
private_key = "0b4df868a1b28fe02836d06c35f8424f1812a8ffeae7ef999ae14a7162365b13"  # MINTER_ROLEを持つウォレットの秘密鍵
to_address = "0x4E201833d980D6d022fFca4Fabcb4Fe9a1e31917"  # NFTを受け取るアドレス
token_uri = "https://ipfs.yamada.jo.sus.ac.jp/ipfs/QmU2gFym7mVEPrxTm3rY1BYsoaEJRajTJiqu4EXreCvHFC"  # NFTのメタデータURI

# コントラクトのABI（例として一部のみを記載。完全なABIを使用してください）
import json

# Hardhatで生成されたJSONファイルを開く
with open('Ferry_NFT.sol/FBT.json', 'r') as contract_file:
    contract_data = json.load(contract_file)
    abi = contract_data['abi']

# Web3インスタンス作成
web3 = Web3(Web3.HTTPProvider(node_url))

# コントラクトインスタンス作成
contract = web3.eth.contract(address=contract_address, abi=abi)

# 送信元アカウントを作成
account = Account.from_key(private_key)
from_address = account.address

# 現在の推奨ガス価格を取得
current_gas_price = web3.eth.gas_price
print(f"Current gas price: {current_gas_price}")

# トランザクション作成時に使用
transaction = contract.functions.safeMint(to_address, token_uri).build_transaction({
    'from': from_address,
    'nonce': web3.eth.getTransactionCount(from_address),
    'gas': 2000000,
    'gasPrice': current_gas_price,
})

# トランザクション署名
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# トランザクション送信
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# トランザクションハッシュの表示
print(f"Transaction sent! Hash: {txn_hash.hex()}")

# トランザクション完了の確認
txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction confirmed! Receipt: {txn_receipt}")