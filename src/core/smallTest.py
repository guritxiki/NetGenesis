import struct
import time
from transaction import *
from wallet import *
from block import *
from script import *
from block import *


# Constants
COINBASE_REWARD = 50 * 10**8  # 50 coins, assuming 8 decimal places

# Create two wallets
wallet1 = Wallet() # wallet to which the coinbase transaction is sent, and which will sign a new transaction
privKey1, pubKey1 = wallet1.generate_keypair_from_string("Guria")
address1 = wallet1.public_key_to_address(pubKey1)
public_key_hash1 = wallet1.address_to_pubkey_hash(address1)
scriptPubKey = Script.createP2PKH_ScriptPubKey(public_key_hash1)

# Wallet that will recieve the next transaction
wallet2 = Wallet()
privKey2, pubKey2 = wallet2.generate_keypair_from_string("Alice")
address2 = wallet2.public_key_to_address(pubKey2)
public_key_hash2 = wallet2.address_to_pubkey_hash(address2)




# Main test
if __name__ == "__main__":
    # Create genesis block

    genesisBlock = Block.generateGenesisBlock(public_key_hash1)
    print("Genesis Block created:")
    print(genesisBlock.to_json())

    # Create a transaction spending from the coinbase
    coinbase_tx = genesisBlock.transactions[0]
    spending_tx = wallet1.createSpendingTransaction(
        prev_tx=coinbase_tx,
        prev_output_index=0,
        value=25 * 10**8,  # Send 25 coins
        to_address=address2
    )

    print("\nSpending Transaction created:")
    print(spending_tx.to_json())

    print("Second transaction")
    secondTransacation = wallet2.createSpendingTransaction(
        prev_tx=spending_tx,
        prev_output_index=0,
        value=25 * 10**8,  # Send 25 coins
        to_address=address2
    )
    print(secondTransacation.to_json())
