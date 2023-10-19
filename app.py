from flask import Flask, render_template, request, redirect
from web3 import Web3
import json

abi = json.loads('[{"inputs":[{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"addEntry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"entries","outputs":[{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEntries","outputs":[{"components":[{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct Ledger.Entry[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]')

contract_address = "0x57F6eBc68ED66417f09e832cb98fA50c48bcb432"  # Replace with your contract address
private_key = "051b7dab0e5d6cc6c0a41fa2daecb99ef16ba0e38901ecaef8bc0720c485aa11"  # Replace with your private key

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/734ed36cb57348b39159e09139f3fc10"))

contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route("/")
def index():
    entries = contract.functions.getEntries().call()
    return render_template("index.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    description = request.form["description"]
    amount = request.form["amount"]
    amt=int(float(amount))

    sender_address = "0xD4cd86fC20602Bb54bb76A6052b8a716B1837e79"  # Replace with the sender's Ethereum address

    nonce = w3.eth.get_transaction_count(sender_address)

    transaction = contract.functions["addEntry"](description, amt).build_transaction({
        'chainId': 5,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'from': sender_address
    })

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    entries = contract.functions["getEntries"].call({'from':sender_address})

    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
