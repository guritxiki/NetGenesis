import hashlib
import ecdsa
import base58

def generate_keypair_from_string(seed_string):
    # Hash the seed string using SHA-256
    seed_hash = hashlib.sha256(seed_string.encode('utf-8')).digest()

    # Use the hash as the private key
    priv_key = ecdsa.SigningKey.from_string(seed_hash, curve=ecdsa.SECP256k1)
    pub_key = priv_key.get_verifying_key()
    return priv_key, pub_key

def public_key_to_address(pub_key):
    # Convert public key to bytes
    pub_key_bytes = pub_key.to_string()

    # Perform SHA-256 followed by RIPEMD-160
    sha256 = hashlib.sha256(pub_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()

    # Add version byte (0x00 for P2PKH)
    versioned_payload = b'\x00' + ripemd160

    # Perform double SHA-256 and get the checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]

    # Encode the address in Base58Check format
    address = base58.b58encode(versioned_payload + checksum)
    return address.decode('utf-8')

if __name__ == "__main__":
    seed_string = "example_seed_string"
    priv_key, pub_key = generate_keypair_from_string(seed_string)
    address = public_key_to_address(pub_key)
    print(f"Seed String: {seed_string}")
    print(f"Private Key (hex): {priv_key.to_string().hex()}")
    print(f"Public Key (hex): {pub_key.to_string().hex()}")
    print(f"P2PKH Address: {address}")
