import subprocess
from constants import *
import os
import json
import bit
from bit import wif_to_key
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pathlib import Path
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

mnemonic = os.getenv("MNEMONIC")
num_keys=1
coin_request = BTCTEST

#create a function to get wallet keys
def derive_wallets(mnemonic, num_keys, coin_request):
    command = f'php derive -g --mnemonic="{mnemonic}"" --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --coin={coin_request} --numderive={num_keys} --format==json'
    p = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    coin_info = json.loads(output)
    return coin_info

#create a wallet of ETH and BTC-test coins
wallet = derive_wallets(mnemonic, num_keys, coin_request)
coins = {BTCTEST:[], ETH: []}
coins[BTCTEST].append(wallet)
coin_request = ETH
wallet = derive_wallets(mnemonic, num_keys, coin_request)
coins[ETH].append(wallet)

#create a function that converts private key into an account address
def priv_key_to_account(coin):
    if coin == BTCTEST:
        priv_key= coins[BTCTEST][0]['privkey']
        return bit.PrivateKeyTestnet(priv_key)
    if coin == ETH:
        priv_key = coins[ETH][0]['privkey']
        pub_address =web3.Account.privateKeyToAccount(priv_key)
        return pub_address.address

#create a function to create a raw transaction    
def create_tx(coin, account, recipient, amount):
    account = priv_key_to_account(account)
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({"from": account, "to": recipient, "value": amount}
        )
        return {
            "from": account,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account),
        }
    if coin == BTCTEST:
        tx = bit.PrivateKeyTestnet.prepare_transaction(account, [(recipient, amount, BTCTEST)])
        return tx 

#create a function to send a raw transaction    
def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    if coin == ETH:
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    
    if coin == BTCTEST:
        signed_tx = bit.PrivateKeyTestnet.sign_transaction(tx)
        result = bit.NetworkAPI.broadcast_tx_testnet(signed_tx)
        print(result.hex())
        return result.hex()
