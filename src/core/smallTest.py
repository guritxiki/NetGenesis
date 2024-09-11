import struct
from transaction import *
from wallet import *
from block import *
from script import *



#  50 coins as the value (in your blockchain's smallest unit)
COINBASE_REWARD = 50 * 10**8  # Assuming 8 decimal places like Bitcoin


# Wallet where bitcoins will be sent to
privKey,pubKey = Wallet.generate_keypair_from_string("Guria")
adress = Wallet.public_key_to_address(pub_key)
public_key_hash = Wallet.address_to_pubkey_hash(address)

P2PKH_ScriptPubKey= Script.create_p2pkh_scriptpubkey(public_key_hash)

# Create a coin output with 50 coins and the provided scriptPubKey (public key hash)
coin_output = CoinOutput(value=COINBASE_REWARD, script_pub_key=public_key_hash)

# Create a coinbase transaction
coinbase_tx = CoinbaseTransaction(
    version=1,           # Transaction version
    outputs=[coin_output],  # List containing the single output of 50 coins
    lock_time=0          # Set lock_time to 0 for simplicity
)

# Serialize the coinbase transaction
serialized_tx = coinbase_tx.serialize()

# Output the serialized coinbase transaction
print("Serialized Coinbase Transaction:", serialized_tx.hex())

# Deserialize the transaction (for demonstration purposes)
deserialized_tx = CoinbaseTransaction.parse(serialized_tx)

# Print the deserialized transaction in JSON format
print("Deserialized Coinbase Transaction:", deserialized_tx.to_json())
