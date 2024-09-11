import hashlib
import ecdsa
import base58
from script import *

import hashlib
import base58
import ecdsa
import os

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None

    def generate_keypair_from_string(self, seed_string):
        """
        Generate a keypair from a given seed string.
        """
        seed_hash = hashlib.sha256(seed_string.encode('utf-8')).digest()
        priv_key = ecdsa.SigningKey.from_string(seed_hash, curve=ecdsa.SECP256k1)
        pub_key = priv_key.get_verifying_key()
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
    seed_string = "example_seed_string"
    priv_key, pub_key = generate_keypair_from_string(seed_string)
    address = public_key_to_address(pub_key)
    print(f"Seed String: {seed_string}")
    print(f"Private Key (hex): {priv_key.to_string().hex()}")
    print(f"Public Key (hex): {pub_key.to_string().hex()}")
    print(f"P2PKH Address: {address}")
    print(f"-----------Now Lets create a P2PKH-----------")
    # Example of creating a P2PKH
    print(address)
    P2PKH = Script.create_p2pkh_scriptpubkey(address_to_pubkey_hash(address))
    print(P2PKH)
