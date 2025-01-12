import requests

BASE_URL = "http://127.0.0.1:5000"  # Change this to your server's URL if needed

class BlockchainAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def create_wallet(self):
        response = requests.get(f"{self.base_url}/wallet/new")
        if response.status_code == 200:
            wallet_data = response.json()
            return wallet_data
        else:
            raise Exception("Failed to create wallet")

    def send_transaction(self, sender_address, sender_private_key, amount, recipient_address):
        transaction_data = {
            "sender": sender_address,
            "receiver": recipient_address,
            "amount": amount,
            "private_key": sender_private_key
        }
        response = requests.post(f"{self.base_url}/transaction/new", json=transaction_data)
        if response.status_code == 201:
            return "Transaction created successfully"
        else:
            raise Exception(response.text)

    def mine_block(self, miner_address):
        response = requests.get(f"{self.base_url}/mine?miner={miner_address}")
        if response.status_code == 200:
            return "Block mined successfully"
        else:
            raise Exception("Failed to mine block")

    def get_wallet_balance(self, wallet_address):
        response = requests.get(f"{self.base_url}/wallet/balance?address={wallet_address}")
        if response.status_code == 200:
            balance_data = response.json()
            return balance_data['balance']
        else:
            raise Exception("Failed to retrieve wallet balance")

# Usage example
if __name__ == "__main__":
    api = BlockchainAPI()

    # Create a new wallet
    wallet_data = api.create_wallet()
    print(f"Created Wallet Address: {wallet_data['wallet_address']}")
    print(f"Private Key: {wallet_data['private_key']}")

    # Create another wallet for the recipient
    recipient_wallet_data = api.create_wallet()
    print(f"Recipient Wallet Address: {recipient_wallet_data['wallet_address']}")

    # Send coins
    sender_address = wallet_data['wallet_address']
    sender_private_key = wallet_data['private_key']
    recipient_address = recipient_wallet_data['wallet_address']
    amount = 10

    print(api.send_transaction(sender_address, sender_private_key, amount, recipient_address))

    # Mine a block
    print(api.mine_block(sender_address))

    # Get wallet balances
    sender_balance = api.get_wallet_balance(sender_address)
    print(f"Sender Balance: {sender_balance}")

    recipient_balance = api.get_wallet_balance(recipient_address)
    print(f"Recipient Balance: {recipient_balance}")
