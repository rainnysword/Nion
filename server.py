"""
Thy Blockchain
"""
from flask import Flask, jsonify, request
from utils.block import *
from utils.blockchain import *


# Initialize Flask app

# Initialize Flask app
app = Flask(__name__)

# Initialize blockchain
blockchain = Blockchain()

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    wallet_address, private_key = blockchain.create_wallet()
    response = {'wallet_address': wallet_address, 'private_key': private_key}
    return jsonify(response), 200

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'receiver', 'amount', 'private_key']
    if not all(k in values for k in required):
        return 'Missing values', 400
    result = blockchain.create_transaction(values['sender'], values['receiver'], values['amount'], values['private_key'])
    if result == "Transaction created":
        return 'Transaction created', 201
    else:
        return result, 400

@app.route('/register', methods=['POST'])
def register_miner():
    values = request.get_json()
    required = ['miner_address']
    if not all(k in values for k in required):
        return 'Missing values', 400
    if blockchain.register_miner(values['miner_address']):
        return 'Miner registered', 201
    else:
        return 'Miner already registered', 400

@app.route('/mine', methods=['GET'])
def mine():
    miner_address = request.args.get('miner')
    blockchain.mine_pending_transactions(miner_address)
    return 'Block mined', 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.__dict__ for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/wallet/balance', methods=['GET'])
def wallet_balance():
    wallet_address = request.args.get('address')
    balance = blockchain.get_wallet_balance(wallet_address)
    response = {'wallet_address': wallet_address, 'balance': balance}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
