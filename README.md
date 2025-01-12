# Nion Blockchain

## Overview

This blockchain system is a decentralized and transparent digital ledger of transactions managed by a distributed network of computers. Each computer, or node, in the network participates in the verification of transactions and helps maintain the integrity and security of the blockchain. This implementation includes a mining pool system, wallet management, and transaction verification features.

## Key Features

1. **Genesis Block:**
   - The blockchain begins with a genesis block, which serves as the foundation of the chain. This block contains default data and marks the start of the blockchain.

2. **Wallet Management:**
   - **Wallet Creation:** Users can create new wallets, each containing a unique public-private key pair generated using elliptic curve cryptography (ecdsa).
   - **Persistent Storage:** Wallets are stored in a JSON file (`wallets.json`) to ensure data persistence across server restarts.
   - **Balance Management:** Each wallet maintains its balance, and transactions update wallet balances accordingly.

3. **Transaction Handling:**
   - **Creating Transactions:** Users can create transactions specifying the sender, receiver, amount, and private key for signing.
   - **Signature Verification:** Each transaction is signed by the sender's private key and verified by the receiver's public key, ensuring authenticity and integrity.
   - **Cents to Dollars Conversion:** The system ensures that fractional amounts are converted into dollar amounts for consistency in transactions.

4. **Mining Process:**
   - **Proof of Work:** The mining process involves solving a cryptographic puzzle using the proof of work (PoW) algorithm.
   - **Mining Pool:** The implementation supports a mining pool where multiple miners collaborate to solve the PoW. When a block is mined successfully, rewards are distributed equally among all miners in the pool.
   - **Reward Distribution:** The reward for mining is taken from a designated wallet (`'0'`), and 1 unit of fund is divided equally among the miners.

5. **Blockchain Integrity:**
   - **Block Validation:** Each new block is validated by ensuring it contains the correct index, previous hash, and valid hash.
   - **Chain Continuity:** The blockchain maintains continuity by ensuring that each new block points back to the previous block, forming an unbroken chain.

6. **API Endpoints:**
   - **New Wallet Endpoint:** Creates a new wallet and returns the wallet address and private key.
   - **New Transaction Endpoint:** Creates a new transaction based on the provided sender, receiver, amount, and private key.
   - **Register Miner Endpoint:** Registers a miner in the mining pool.
   - **Mine Block Endpoint:** Initiates the mining process for pending transactions.
   - **Full Chain Endpoint:** Retrieves the entire blockchain for inspection.
   - **Wallet Balance Endpoint:** Retrieves the balance of a specified wallet.

This repository also comes with an API wrapper if you want to create your own wallet.

## Usage

To interact with the blockchain, users can make requests to the various endpoints to create wallets, submit transactions, register miners, mine blocks, and query the blockchain.
