import hashlib
import ecdsa
import base58
import os
from script import *
from transaction import *

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None

    def generate_keypair_from_string(self, seed_string):
        """
        Generate a keypair from a given seed string by hashing it with SHA-256
        and using the 256-bit hash as the private key.
        """
        # Hash the seed string with SHA-256
        seed_hash = hashlib.sha256(seed_string.encode('utf-8')).digest()
        # Use the hash as the private key
        priv_key = ecdsa.SigningKey.from_string(seed_hash, curve=ecdsa.SECP256k1)
        # Get the corresponding public key
        pub_key = priv_key.get_verifying_key()
        # Store the private key, public key, and address
        self.private_key = priv_key
        self.public_key = pub_key
        self.address = self.public_key_to_address(pub_key)
        
        return priv_key, pub_key

    def generate_random_keypair(self):
        """
        Generate a random keypair.
        """
        priv_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        pub_key = priv_key.get_verifying_key()
        self.private_key = priv_key
        self.public_key = pub_key
        self.address = self.public_key_to_address(pub_key)
        return priv_key, pub_key

    def public_key_to_address(self, pub_key):
        """
        Convert a public key to a Base58Check encoded address.
        """
        pub_key_bytes = pub_key.to_string()
        sha256 = hashlib.sha256(pub_key_bytes).digest()
        ripemd160 = hashlib.new('ripemd160', sha256).digest()
        versioned_payload = b'\x00' + ripemd160
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        address = base58.b58encode(versioned_payload + checksum)
        return address.decode('utf-8')

    def address_to_pubkey_hash(self, address):
        """
        Convert a Base58Check encoded address to a public key hash.
        """
        decoded = base58.b58decode_check(address)
        pubkey_hash = decoded[1:]
        return pubkey_hash
    def sign_message(self, message: bytes) -> bytes:
        """
        Sign a message using the private key associated with this wallet.
        
        :param message: The message to sign, typically a byte representation of the transaction hash.
        :return: The signature of the message.
        """
        if not self.private_key:
            raise ValueError("No private key set for signing")
        return self.private_key.sign(message, hashfunc=hashlib.sha256)
    
    def createSpendingTransaction(self, prev_tx: 'Transaction', prev_output_index: int, value: int, to_address: str) -> 'Transaction':
        """
        Create a spending transaction.

        :param prev_tx: The previous transaction from which the output is being spent.
        :param prev_output_index: The index of the output in the previous transaction being spent.
        :param value: The amount to be transferred.
        :param to_address: The address of the recipient.
        :return: A new transaction that spends from the previous transaction to the new address.
        """
        # Create input
        txid = hashlib.sha256(prev_tx.serialize()).digest() # Acts as the message that has to be signed in order to make a valid ScripSig
        signature = self.sign_message(txid)  # Use the wallet's private key to sign the transaction hash
        scriptSig = Script.createP2PKH_ScriptSig(signature,self.public_key)
        coin_input = CoinInput(txid, prev_output_index, scriptSig)

        # Create output
        to_public_key_hash = self.address_to_pubkey_hash(to_address)
        scriptPubKey = Script.createP2PKH_ScriptPubKey(to_public_key_hash)
        coin_output = CoinOutput(value, scriptPubKey)

        # Create transaction
        tx = Transaction(
            tx_type=1,  # Regular transaction
            version=1,
            coin_inputs=[coin_input],
            coin_outputs=[coin_output],
            lock_time=0
        )

        return tx

    def to_json(self):
        """
        Convert the wallet details to a JSON-compatible dictionary.
        """
        return {
            'private_key': self.private_key.to_string().hex() if self.private_key else None,
            'public_key': self.public_key.to_string().hex() if self.public_key else None,
            'address': self.address
        }














if __name__ == "__main__":
    wallet = Wallet()
    seed_string = "example_seed_string"
    priv_key, pub_key = wallet.generate_keypair_from_string(seed_string)
    address = wallet.public_key_to_address(pub_key)
    print(f"Seed String: {seed_string}")
    print(f"Private Key (hex): {priv_key.to_string().hex()}")
    print(f"Public Key (hex): {pub_key.to_string().hex()}")
    print(f"P2PKH Address: {address}")
    print(f"-----------Now Lets create a P2PKH-----------")
    # Example of creating a P2PKH
    print(address)
    P2PKH = Script.createP2PKH_ScriptPubKey(wallet.address_to_pubkey_hash(address))
    print(P2PKH)
