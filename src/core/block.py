import json
import struct
import hashlib
from transaction import *

class Block:
    def __init__(self, version, previous_hash, merkle_root, timestamp, difficulty, nonce, transactions):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty = difficulty  # Changed from bits to difficulty
        self.nonce = nonce
        self.transactions = transactions

    def serialize(self):
        version_bin = struct.pack('>I', self.version)
        previous_hash_bin = self.previous_hash
        merkle_root_bin = self.merkle_root
        timestamp_bin = struct.pack('>I', self.timestamp)
        difficulty_bin = struct.pack('>I', self.difficulty)  # Changed from bits to difficulty
        nonce_bin = struct.pack('>I', self.nonce)
        transactions_bin = b''.join(tx.serialize() for tx in self.transactions)
        
        return version_bin + previous_hash_bin + merkle_root_bin + timestamp_bin + difficulty_bin + nonce_bin + transactions_bin

    @staticmethod
    def parse(data):
        offset = 0
        version = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        previous_hash = data[offset:offset+32]
        offset += 32
        merkle_root = data[offset:offset+32]
        offset += 32
        timestamp = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        difficulty = struct.unpack('>I', data[offset:offset+4])[0]  # Changed from bits to difficulty
        offset += 4
        nonce = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4

        transactions = []
        while offset < len(data):
            tx = Transaction.parse(data[offset:])
            transactions.append(tx)
            offset += len(tx.serialize())
        
        return Block(version, previous_hash, merkle_root, timestamp, difficulty, nonce, transactions)

    def to_json(self):
        return {
            'version': self.version,
            'previous_hash': self.previous_hash.hex(),
            'merkle_root': self.merkle_root.hex(),
            'timestamp': self.timestamp,
            'difficulty': self.difficulty,  # Changed from bits to difficulty
            'nonce': self.nonce,
            'transactions': [tx.to_json() for tx in self.transactions]
        }

    @staticmethod
    def calculateMerkleRoot(transactions):
        """
        Calculate the Merkle root of the transactions.
        """
        if not transactions:
            return b'\x00' * 32
        
        def hash_pair(left, right):
            return hashlib.sha256(hashlib.sha256(left + right).digest()).digest()
        
        # Get the hashes of all transactions
        tx_hashes = [hashlib.sha256(tx.serialize()).digest() for tx in transactions]
        
        # If there is only one hash, it is the Merkle root
        if len(tx_hashes) == 1:
            return tx_hashes[0]
        
        # If there is an odd number of hashes, duplicate the last one
        if len(tx_hashes) % 2 != 0:
            tx_hashes.append(tx_hashes[-1])
        
        # Calculate the Merkle root
        while len(tx_hashes) > 1:
            new_level = []
            for i in range(0, len(tx_hashes), 2):
                new_level.append(hash_pair(tx_hashes[i], tx_hashes[i+1]))
            tx_hashes = new_level
        
        return tx_hashes[0]

    @staticmethod
    def generateGenesisBlock(scriptPubKey):
        """
        Generate the Genesis block with a single coinbase transaction.
        """
        INITIAL_COINBASE_REWARD = 50 * 10**8
        # Define the parameters for the Genesis block
        version = 1
        previous_hash = b'\x00' * 32
        timestamp = 1234567890  # Example timestamp
        difficulty = 0x1d00ffff  # Example difficulty
        nonce = 0  # Starting nonce

        # Create a coinbase transaction with an output to the given scriptPubKey
        coinbase_tx = Transaction(
            tx_type=0,  # Coinbase transaction
            version=1,
            coin_inputs=[],
            coin_outputs=[CoinOutput(INITIAL_COINBASE_REWARD, scriptPubKey)],  # Example value
            lock_time=0
        )
        
        # Calculate the Merkle root
        merkle_root = Block.calculateMerkleRoot([coinbase_tx])
        
        # Create the Genesis block
        genesis_block = Block(
            version=version,
            previous_hash=previous_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            difficulty=difficulty,  # Changed from bits to difficulty
            nonce=nonce,
            transactions=[coinbase_tx]
        )
        
        return genesis_block

    