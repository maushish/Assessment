from flask import Flask, render_template, request, redirect
from web3 import Web3
from dotenv import load_dotenv
import os
import json

load_dotenv()

infura_api = os.getenv("INFURA_API")
abi = json.loads('''[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "addEntry",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "entries",
		"outputs": [
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getEntries",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "description",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "amount",
						"type": "uint256"
					}
				],
				"internalType": "struct Ledger.Entry[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]''')


contract_add = os.getenv("ADD")
key = os.getenv("PVT_KEY")


app = Flask(__name__)

@app.route("/")
def index():
    w3 = Web3(Web3.HTTPProvider(infura_api))

    contract_address = contract_add 
    contract = w3.eth.contract(address=contract_address, abi=abi)  

    entries = contract.functions.getEntries().call()

    return render_template("index.html" , entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    description = request.form["description"]
    amount = int(request.form["amount"])

    w3 = Web3(Web3.HTTPProvider(infura_api))

    contract_address = contract_add  
    contract = w3.eth.contract(address=contract_address, abi=abi)  

    tx = contract.functions.addEntry(description, amount).buildTransaction()
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=key)
    w3.eth.send_transaction(signed_tx)

    entries = contract.functions.getEntries().call()

    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
