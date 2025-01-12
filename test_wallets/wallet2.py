import requests

BASE_URL = "http://127.0.0.1:5000"  # Change this to your server's URL if needed

class BlockchainAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

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

   
    recipient_address = "1"  # Replace this with actual recipient wallet address

    # Get and print recipient wallet balance
    recipient_balance = api.get_wallet_balance(recipient_address)
    print(f"Recipient Balance: {recipient_balance}")
