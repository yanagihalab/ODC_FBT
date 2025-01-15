from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from web3 import Web3
import os
import json
import config

node_url = config.NODE_URL

config.TOKEN_URI

app = Flask(__name__)
app.secret_key = 'your_sec
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ethereum Node Connection

web3 = Web3(Web3.HTTPProvider(node_url))

if not web3.isConnected():
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

@app.route('/mint_nft', methods=['GET', 'POST'])
def mint_nft():
    if request.method == 'POST':
        nft_name = request.form['nft_name']
        nft_image = ret_key'request.files['nft_image']

        if nft_name and nft_image:
            # Save the image
            filename = secure_filename(nft_image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                nft_image.save(filepath)
            except Exception as e:
                flash(f"Failed to save image: {str(e)}", 'danger')
                return render_template('mint_nft.html')

            # Interact with the Ethereum blockchain
            try:
                wallet_private_key = config.P_KEY
                wallet_address = config.W_ADRESS 

                if not wallet_private_key or not wallet_address:
                    raise Exception("Wallet credentials are missing. Ensure WALLET_PRIVATE_KEY and WALLET_ADDRESS are set.")

                # Simulating IPFS URI
                token_uri = f"https://ipfs.yourdomain.com/{filename}"

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
            flash("Please provide both NFT name and image.", 'warning')

    return render_template('mint_nft.html')

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)

# https://www.oklink.com/ja/amoy/token/0x56d8cb8824caa15e76206276a5108de0e7386d77