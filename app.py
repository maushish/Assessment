from flask import Flask, render_template, request, redirect
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

infura_api=os.getenv("INFURA_API")
abi=os.getenv("ABI")
add=os.getenv("ADD")




app = Flask(__name__, template_folder='templates')
@app.route("/")
def index():
    w3 = Web3(Web3.HTTPProvider("infura_api"))

    contract_address = "add"
    abi = "ABI"

    contract = w3.eth.contract(address=contract_address, abi=abi)

    entries = contract.functions.getEntries().call()

    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    description = request.form["description"]
    amount = int(request.form["amount"])

    w3 = Web3(Web3.HTTPProvider(infura_api))

    contract_address = "add"
    abi = "ABI"

    contract = w3.eth.contract(address=contract_address, abi=abi)

    tx = contract.functions.addEntry(description, amount).buildTransaction()
    signed_tx = w3.eth.account.sign_transaction(tx, private_key="<YOUR_PRIVATE_KEY>")
    w3.eth.send_transaction(signed_tx)

    entries = contract.functions.getEntries().call()

    return render_template("index.html", entries=entries)


if __name__ =="__main__":
    app.run(debug=True)