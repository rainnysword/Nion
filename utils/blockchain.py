import hashlib
import time
import json
import ecdsa
import random
from utils.block import *

class Blockchain:
    def __init__(self, difficulty=1, wallets_file="wallets.json"):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.wallets_file = wallets_file
        self.wallets = self.load_wallets()
        self.difficulty = difficulty
        self.miners_pool = []  # List of miners in the pool

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", 0)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        if self.is_valid_new_block(block, self.get_last_block()):
            self.chain.append(block)

    def load_wallets(self):
        try:
            with open(self.wallets_file, 'r') as file:
                wallets = json.load(file)
                return wallets
        except FileNotFoundError:
            return {
                '0': {
                    'balance': 67,
                    'private_key': 'b7c6d18669ec69fa071d6b0ae10823600faad0b0ced9bac4341ee799132e214d'
                },
                '1': {
                    'balance': 5,
                    'private_key': 'b7c6d18669ec69fa071d6b0ae10823600faad0b0ced9bac4341ee799132e214e'
                }
            }

    def save_wallets(self):
        with open(self.wallets_file, 'w') as file:
            json.dump(self.wallets, file)

    def create_wallet(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        wallet_address = public_key.to_string().hex()
        self.wallets[wallet_address] = {
            'balance': 0.0,
            'private_key': private_key.to_string().hex()
        }
        self.save_wallets()
        return wallet_address, private_key.to_string().hex()

    def sign_transaction(self, private_key, transaction):
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        message = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}"
        signature = sk.sign(message.encode()).hex()
        return signature

    def verify_transaction(self, transaction, signature):
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(transaction['sender']), curve=ecdsa.SECP256k1)
        message = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}"
        return vk.verify(bytes.fromhex(signature), message.encode())

    def create_transaction(self, sender, receiver, amount, private_key):
        dollar_amount = round(amount, 2)
        if dollar_amount <= 0:
            return "Amount must be greater than zero"
        if sender in self.wallets and self.wallets[sender]['balance'] >= dollar_amount:
            transaction = {"sender": sender, "receiver": receiver, "amount": dollar_amount}
            signature = self.sign_transaction(private_key, transaction)
            transaction['signature'] = signature

            # Update wallet balances and save changes
            self.wallets[sender]['balance'] -= dollar_amount
            if receiver in self.wallets:
                self.wallets[receiver]['balance'] += dollar_amount
            else:
                self.wallets[receiver] = {
                    'balance': dollar_amount,
                    'private_key': None
                }
            self.save_wallets()

            self.pending_transactions.append(transaction)
            return "Transaction created"
        else:
            return "Insufficient funds or invalid sender address"

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def mine_pending_transactions(self, miner_address):
        last_block = self.get_last_block()
        last_proof = last_block.proof
        proof = self.proof_of_work(last_proof)

        block = Block(len(self.chain), last_block.hash, time.time(), self.pending_transactions, proof)
        self.add_block(block)

        # Clear pending transactions after mining
        self.pending_transactions = []

        # Add miner to pool if not already in it
        if miner_address not in self.miners_pool:
            self.miners_pool.append(miner_address)

        # Distribute reward from wallet '0' amongst all miners in the pool
        sender = '0'
        amount = 1
        private_key = self.wallets[sender]['private_key']

        for miner in self.miners_pool:
            transaction = {"sender": sender, "receiver": miner, "amount": amount / len(self.miners_pool)}
            signature = self.sign_transaction(private_key, transaction)
            transaction['signature'] = signature
            self.wallets[sender]['balance'] -= transaction['amount']
            self.wallets[miner]['balance'] += transaction['amount']

        self.save_wallets()

    def get_wallet_balance(self, wallet_address):
        if wallet_address in self.wallets:
            return self.wallets[wallet_address]['balance']
        return 'Wallet not found'

    def is_valid_new_block(self, new_block, previous_block):
        if previous_block.index + 1 != new_block.index:
            return False
        if previous_block.hash != new_block.previous_hash:
            return False
        if new_block.hash != new_block.calculate_hash():
            return False
        return True

