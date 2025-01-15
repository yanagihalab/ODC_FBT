from web3 import Web3
import json
# Web3インスタンス作成
node_url = "https://polygon-amoy.g.alchemy.com/v2/Z_HZ6k3vLbqJom0WbQym1U3yHO-T34Lh"
web3 = Web3(Web3.HTTPProvider(node_url))

# トランザクション送信ハッシュ
txn_hash = "0x4106e784024299ca40274a2841d640358e8665ecf96d694611688a5a6174162f"
print(f"Transaction sent! Hash: {txn_hash}")

# トランザクション完了の確認
txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

# コントラクトインスタンス作成
contract_address = "0x56D8CB8824CAA15E76206276A5108DE0E7386D77"
# Hardhatで生成されたJSONファイルを開く
with open('Ferry_NFT.sol/FBT.json', 'r') as contract_file:
    contract_data = json.load(contract_file)
    abi = contract_data['abi']  # コントラクトのABIを挿入
contract = web3.eth.contract(address=contract_address, abi=abi)

# イベントログを解析してトークンIDを取得
logs = txn_receipt.logs
token_id = None
for log in logs:
    try:
        decoded_log = contract.events.Transfer().processLog(log)
        token_id = decoded_log['args']['tokenId']
        print(f"Minted Token ID: {token_id}")
        break
    except Exception as e:
        print(f"Log parsing error: {e}")

# トークンURIを取得
if token_id is not None:
    token_uri = contract.functions.tokenURI(token_id).call()
    print(f"Token URI: {token_uri}")
else:
    print("Token ID could not be found.")
