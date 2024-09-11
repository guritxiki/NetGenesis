import struct
from block import Block
from transaction import CoinbaseTransaction

class GenesisBlock(Block):
    def __init__(self):
        # Define the genesis block parameters
        version = 1
        prev_block_hash = b'\x00' * 32  # Genesis block has no previous block
        merkle_root = b'\x00' * 32  # Placeholder for Merkle Root
        timestamp = 1234567890  # Example timestamp
        bits = 0x1d00ffff  # Example difficulty target
        nonce = 2083236893  # Example nonce value
        
        # Define Coinbase Transaction
        coinbase_output_count = 1
        coinbase_outputs = [
            (50 * 10**8, b'\x76\xa9\x14' +  # Example ScriptPubKey (Pay-to-PubKey-Hash)
             bytes.fromhex('1D6kXmzRL6eyFgUt8zcmbtSwKrzt1gaPJf') +
             b'\x88\xac')  # P2PKH ScriptPubKey
        ]
        coinbase_lock_time = 0
        
        # Create Coinbase Transaction
        coinbase_tx = CoinbaseTransaction(
            version=1,
            output_count=coinbase_output_count,
            outputs=coinbase_outputs,
            lock_time=coinbase_lock_time
        )
        
        # Initialize Block with the Coinbase Transaction
        super().__init__(
            version=version,
            prev_block_hash=prev_block_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            bits=bits,
            nonce=nonce,
            transactions=[coinbase_tx]
        )

    def serialize(self):
        # Override serialize method to ensure genesis block specifics
        return super().serialize()

    def parse(self, raw_block):
        # Override parse method if needed
        return super().parse(raw_block)

# Example usage
if __name__ == "__main__":
    genesis_block = GenesisBlock()
    serialized_block = genesis_block.serialize()
    print("Serialized Genesis Block:", serialized_block.hex())
