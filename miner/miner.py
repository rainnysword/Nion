import requests
import time

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

# Miner script
if __name__ == "__main__":
    api = BlockchainAPI()

    # Create a miner wallet
    miner_address = ""
    print(f"[-] Miner Wallet Address: {miner_address}")

    # Start mining indefinitely
    try:
        while True:
            try:
                print("[-] Attempting to mine a new block...")
                mine_status = api.mine_block(miner_address)
                print(mine_status)
                balance = api.get_wallet_balance(miner_address)
                print(f"[/] Current Balance: {balance}")
            except Exception as e:
                print(f"[X] Error occurred: {e}")
            
            # Wait for a short period before mining the next block
            time.sleep(10)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Mining stopped by user")
