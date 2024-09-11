# Block structure and methods 
import json
import struct
class Block:
    def __init__(self, version, previous_hash, merkle_root, timestamp, bits, nonce, transactions):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.transactions = transactions

    def serialize(self):
        version_bin = struct.pack('>I', self.version)
        previous_hash_bin = self.previous_hash
        merkle_root_bin = self.merkle_root
        timestamp_bin = struct.pack('>I', self.timestamp)
        bits_bin = struct.pack('>I', self.bits)
        nonce_bin = struct.pack('>I', self.nonce)
        transactions_bin = b''.join(tx.serialize() for tx in self.transactions)
        
        return version_bin + previous_hash_bin + merkle_root_bin + timestamp_bin + bits_bin + nonce_bin + transactions_bin

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
        bits = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        nonce = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4

        transactions = []
        while offset < len(data):
            tx = Transaction.parse(data[offset:])
            transactions.append(tx)
            offset += len(tx.serialize())
        
        return Block(version, previous_hash, merkle_root, timestamp, bits, nonce, transactions)

    def to_json(self):
        return {
            'version': self.version,
            'previous_hash': self.previous_hash.hex(),
            'merkle_root': self.merkle_root.hex(),
            'timestamp': self.timestamp,
            'bits': self.bits,
            'nonce': self.nonce,
            'transactions': [tx.to_json() for tx in self.transactions]
        }
