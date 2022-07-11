from matplotlib.font_manager import json_dump
from solcx import compile_standard,install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

#fetch contract code
with open("SimpleContract.sol","r") as file:
    SimpleContract = file.read()

#install sol comp 0.8.0
install_solc('0.8.0')


#compile the contract code => bytecode
compiled_sol = compile_standard(
    {
    "language":"Solidity",
    "sources": {"SimpleContract.sol": {"content":SimpleContract}},
    "settings":{
        "outputSelection":{
            "*":{
                "*": ["abi","metadata","evm.bytecode","evm.sourceMap"]
            }
        }
    }

    },
    solc_version="0.8.0",
)

#save bytecode into json

#incase you wanna save in file
# with open("compiled.json","w") as f:
#     json.dump(compiled_sol,f)

#fetching bytecode
bytecode = compiled_sol["contracts"]["SimpleContract.sol"]["SimpleContract"]["evm"]["bytecode"]["object"]

#fetching abi
abi = compiled_sol["contracts"]["SimpleContract.sol"]["SimpleContract"]["abi"]

#initializing the gateway ;)
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/463b997013e041c19b0cb544405eb04e")) #infura ropsten
chain_id = 3 
addr = "0x0f014DB6e23dcA73822Ad84B9a0A0aA5411dFF1D" #my metamask address
priv_key = os.getenv('PRIVATE_KEY') #my metamask private key

#Build the contract
SimpleCon = w3.eth.contract(abi=abi,bytecode=bytecode)

nonce = w3.eth.getTransactionCount(addr)


transaction = SimpleCon.constructor().buildTransaction({"chainId":chain_id,"gasPrice": w3.eth.gas_price, "from":addr, "nonce":nonce})

#Sign the contract
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=priv_key)

#Send the contract
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print("Contract Deployed!")

print("Lets change the state of contract...")
#interact with contract functions
simple_con = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

#Call => for blue button functions (which don't change state)
#Transactions => for yellow button functions (which change state)

#input name
uname = input("Please enter the name: ")

#call getname function for a previous value
print(simple_con.functions.GetName().call())

#Build
store_name_transaction = simple_con.functions.WriteName(uname).buildTransaction({"chainId":chain_id,"gasPrice": w3.eth.gas_price, "from":addr, "nonce":nonce + 1})

#Sign
signed_store_tx = w3.eth.account.sign_transaction(store_name_transaction,private_key=priv_key)

#Send
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print(simple_con.functions.GetName().call())







