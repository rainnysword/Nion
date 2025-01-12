import hashlib
class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()