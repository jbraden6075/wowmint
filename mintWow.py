import time
from web3 import Web3, HTTPProvider
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from web3.middleware import ExtraDataToPOAMiddleware

# Connect to the Shibarium network with a timeout
def setup_web3():
    shibarium_url = "https://www.shibrpc.com"
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    web3_provider = HTTPProvider(shibarium_url, session=session, request_kwargs={'timeout': 60})
    web3 = Web3(web3_provider)

    # Inject middleware to handle PoA chains
    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Check if connected
    if web3.is_connected():
        print("Connected to Shibarium network")
    else:
        print("Failed to connect to Shibarium network")
        raise ConnectionError("Unable to connect to Shibarium network")

    return web3

# Wallet details
wallet_address = ""
private_key = ""

# Contract details
contract_address = "0x8f4b11d923BbAA6206f3Dd3ff84e8e31bafB49b7"
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "allowance",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "needed",
                "type": "uint256"
            }
        ],
        "name": "ERC20InsufficientAllowance",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "balance",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "needed",
                "type": "uint256"
            }
        ],
        "name": "ERC20InsufficientBalance",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "approver",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidApprover",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "receiver",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidReceiver",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidSender",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "ERC20InvalidSpender",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "OwnableInvalidOwner",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "OwnableUnauthorizedAccount",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "MAX_SUPPLY",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "MINT_AMOUNT",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def check_network_status(web3, interval=10):
    while True:
        if web3.is_connected():
            print("Network is up and running")
            return True
        else:
            print(f"Network is down. Retrying in {interval} seconds...")
            time.sleep(interval)

# Function to interact with the contract with retry mechanism
def send_transaction_with_retry(web3, transaction, private_key, retries=5, delay=5):
    for attempt in range(retries):
        try:
            signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f'Transaction sent with hash: {tx_hash.hex()}')
            return tx_hash
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if "already known" in str(e):
                transaction['nonce'] = web3.eth.get_transaction_count(wallet_address, 'pending') + 1
            elif attempt < retries - 1:
                time.sleep(delay)
                transaction['nonce'] = web3.eth.get_transaction_count(wallet_address, 'pending')
            else:
                print("Max retries reached. Transaction failed.")
                return None

def interact_with_contract(web3, contract):
    while True:
        try:
            # Fetch current gas price
            current_gas_price = web3.eth.gas_price
            # Increase gas price slightly above the current average
            adjusted_gas_price = int(current_gas_price * 1.1)

            # Build the transaction
            transaction = contract.functions.mint().build_transaction({
                'from': wallet_address,
                'nonce': web3.eth.get_transaction_count(wallet_address, 'pending'),
                'gas': 2000000,  # Adjust this value based on your contract's requirements
                'gasPrice': adjusted_gas_price
            })

            # Send the transaction with retry logic
            tx_hash = send_transaction_with_retry(web3, transaction, private_key)
            if tx_hash:
                try:
                    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                    print(f'Transaction receipt: {tx_receipt}')
                except Exception as e:
                    print(f"Failed to get transaction receipt: {e}")
                    check_network_status(web3)
                    time.sleep(10)  # Adjust the delay as needed
            else:
                print("Transaction failed after maximum retries.")
        except Exception as e:
            print(f"Encountered an error while interacting with the contract: {e}")
            check_network_status(web3)
            time.sleep(10)  # Delay before retrying

def main():
    while True:
        try:
            web3 = setup_web3()
            contract = web3.eth.contract(address=contract_address, abi=contract_abi)
            while True:
                interact_with_contract(web3, contract)
                time.sleep(3)  # Delay between transactions
        except Exception as e:
            print(f"Encountered an error: {e}. Restarting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script stopped by user")
