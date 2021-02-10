# wallet_wk19

This repo contains a muli-coin wallet python program that can create security keys to create multiple coin wallets.  It can prepare and send transactions while maintaining private key security by using only public addresses.  By using either the BTC-test or ETH network, users can fund and create test transactions between accounts.  

Included in the repo specific to the wallet building are:
wallet.py - global variables can be chosen here for coin choices and number of keys
constants.py - global coin variables 
screenshot folder- screenshots of transactions

Basic instructions:
Run the wallet.py with desired variables.  Currently it is set to 1 BTC-test and 1 ETH account for the wallet.  Using the send_tx function through a CLI, users can send transactions to existing wallets (if they do not have existing wallets, the wallet.py function can create more keys through num_keys variable).  If they are transacting in the ETH POA chain, this repo also contains all the tools for running a private ETH network- network settings, account addresses and passwords are located in chain config.txt.

Issues:
1. The wallet was able to successfully send ETH transactions from existing account (node1) to the new wallet ETH account but the transaction remains as "pending" despite the balance changing within the accounts.  This has been a documented issue and is shown in txETH screenshot.

2. The wallet is having issues with BTC transactions.  The error "Transactions must have at least one unspent" occurs when sending a transaction within the same wallet (using the same source and recipient address for testing purposes).  As seen from the BTCtestbalance screenshot, the account is active and has a balance from the BTC-test faucet, but the error has not been able to be resolved.  