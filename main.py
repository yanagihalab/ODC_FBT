from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
import os
import json
import config
import math
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ethereum Node Connection
node_url = config.NODE_URL
print(node_url)
web3 = Web3(Web3.HTTPProvider(node_url))

if not web3.is_Connected():
    raise Exception("Unable to connect to Ethereum node")

# Load contract ABI and address
contract_address = "0x56D8CB8824CAA15E76206276A5108DE0E7386D77"
contract_abi_path = 'create_NFT/Ferry_NFT.sol/FBT.json'
if not os.path.exists(contract_abi_path):
    raise FileNotFoundError(f"Contract ABI file not found: {contract_abi_path}")

with open(contract_abi_path, 'r') as contract_file:
    contract_data = json.load(contract_file)
    contract_abi = contract_data['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def toppage():
    return render_template('index.html')

@app.route('/mint_nft', methods=['GET', 'POST'])
def mint_nft():
    if request.method == 'POST':
        nft_name = request.form['nft_name']

        if nft_name:
            # Predefined IPFS URI
            token_uri = config.TOKEN_URI

            # Interact with the Ethereum blockchain
            try:
                wallet_private_key = config.P_KEY
                wallet_address = config.W_ADDRESS

                if not wallet_private_key or not wallet_address:
                    raise Exception("Wallet credentials are missing. Ensure P_KEY and W_ADDRESS are set in config.py.")

                # Get current gas price
                current_gas_price = web3.eth.gas_price

                # Build transaction
                nonce = web3.eth.get_transaction_count(wallet_address)
                transaction = contract.functions.safeMint(wallet_address, token_uri).build_transaction({
                    'from': wallet_address,
                    'nonce': nonce,
                    'gas': 2000000,
                    'gasPrice': current_gas_price,
                })

                # Sign and send transaction
                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=wallet_private_key)
                txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                flash(f"NFT successfully minted! Transaction hash: {txn_hash.hex()}", 'success')
                return redirect(url_for('mint_nft'))

            except Exception as e:
                flash(f"Error minting NFT: {str(e)}", 'danger')

        else:
            flash("Please provide an NFT name.", 'warning')

    return render_template('mint_nft.html')

# 模擬チェックポイント (緯度, 経度)
CHECKPOINTS = [
    {"name": "Checkpoint 1", "latitude": 35.6895, "longitude": 139.6917},  # 東京
    {"name": "Checkpoint 2", "latitude": 34.6937, "longitude": 135.5023},  # 大阪
    {"name": "Checkpoint 3", "latitude": 35.0116, "longitude": 135.7681},  # 京都
]

# ハバースインの公式で距離を計算 (km単位)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 地球の半径 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ハバースインの公式で距離を計算 (km単位)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 地球の半径 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/gps', methods=['GET', 'POST'])
def gps_check():
    try:
        # 模擬位置情報 (緯度, 経度)
        simulation_GPS_list = [
            {"name": "有効な位置情報(航路の位置情報)", "latitude":33.456795, "longitude":132.411776},  
            {"name": "無効な位置情報（大阪）", "latitude": 34.6937, "longitude": 135.5023},  # 大阪
            {"name": "無効な位置情報（東京）", "latitude": 35.6895, "longitude": 139.6917},  # 東京
        ]
        valid_locations = [
            {"name": "Checkpoint 1", "latitude": 33.456795, "longitude": 132.411776},
            {"name": "Checkpoint 2", "latitude": 33.455506, "longitude": 132.407827},
            {"name": "Checkpoint 3", "latitude": 33.454073, "longitude": 132.402849},
            {"name": "Checkpoint 4", "latitude": 33.452068, "longitude": 132.392206},
            # {"name": "Checkpoint 5", "latitude": 33.449777, "longitude": 132.378216},
            # {"name": "Checkpoint 6", "latitude": 33.446793, "longitude": 132.365398},
            # {"name": "Checkpoint 7", "latitude": 33.443713, "longitude": 132.354412},
            # {"name": "Checkpoint 8", "latitude": 33.439201, "longitude": 132.340937},
            # {"name": "Checkpoint 9", "latitude": 33.434665, "longitude": 132.330151},
            # {"name": "Checkpoint 10", "latitude": 33.426427, "longitude": 132.315044},
            # {"name": "Checkpoint 11", "latitude": 33.414105, "longitude": 132.293129},
            # {"name": "Checkpoint 12", "latitude": 33.385443, "longitude": 132.24206},
            # {"name": "Checkpoint 13", "latitude": 33.362458, "longitude": 132.201633},
            # {"name": "Checkpoint 14", "latitude": 33.337412, "longitude": 132.157202},
            # {"name": "Checkpoint 15", "latitude": 33.322209, "longitude": 132.122955},
            # {"name": "Checkpoint 16", "latitude": 33.310016, "longitude": 132.065964},
            # {"name": "Checkpoint 17", "latitude": 33.304134, "longitude": 132.002563},
            # {"name": "Checkpoint 18", "latitude": 33.302986, "longitude": 131.948032},
            # {"name": "Checkpoint 19", "latitude": 33.300978, "longitude": 131.834908},
            # {"name": "Checkpoint 20", "latitude": 33.299399, "longitude": 131.752853},
            # {"name": "Checkpoint 21", "latitude": 33.29696, "longitude": 131.622562},
            # {"name": "Checkpoint 22", "latitude": 33.295956, "longitude": 131.55201},
            # {"name": "Checkpoint 23", "latitude": 33.297821, "longitude": 131.516819},
            # {"name": "Checkpoint 24", "latitude": 33.298395, "longitude": 131.509609}
            ]


        # GET/POST 判定
        if request.method == 'POST':
            # フォームから選択されたチェックポイント
            selected_checkpoint = request.form.get('checkpoint')
            print("HHHHH",selected_checkpoint)
            for GPS in simulation_GPS_list:
                print(GPS['name'])
                if GPS['name'] == selected_checkpoint:
                    print("合致")
                    input_latitude = GPS["latitude"]
                    input_longitude = GPS["longitude"]
            
            for loc in valid_locations:
                print(loc)
                print(loc["latitude"])
                print(loc["latitude"])
                if input_latitude == loc["latitude"] :
                    if input_longitude == loc["longitude"]:
                        flash(f"乗船ありがとうございます。\n 有効な位置情報が確認されました。 乗船記念NFTを発行します。", "success")
                        return redirect(url_for('mint_nft'))  # エンドポイント名 'mint_nft' にリダイレクト
                    else:
                        print("探索中")    
                else:
                    print("探索中")
                                    
            # else:
            #     # 無効な場合は警告メッセージを表示して再レンダリング
            #     flash("有効な位置情報はありませんでした。", "warning")

        # GETリクエストまたは無効な場合
        return render_template('gps_form.html', checkpoints=simulation_GPS_list)

    except Exception as e:
        logger.error(f"Error in GPS check route: {e}")
        flash("サーバーエラーが発生しました。管理者にお問い合わせください。", "danger")
        return render_template('gps_form.html', checkpoints=simulation_GPS_list, results=[])

if __name__ == '__main__':
    app.run(debug=True)
