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

# Usage example
if __name__ == "__main__":
    api = BlockchainAPI()

    # Create a sender wallet
    sender_address = "0"
    sender_private_key = "b7c6d18669ec69fa071d6b0ae10823600faad0b0ced9bac4341ee799132e214d"
    print(f"Sender Wallet Address: {sender_address}")
    print(f"Sender Private Key: {sender_private_key}")

    recipient_address = "1"
    print(f"Recipient Wallet Address: {recipient_address}")

    amount = 0.999
    print(api.send_transaction(sender_address, sender_private_key, amount, recipient_address))

    print(api.mine_block(sender_address))
