import hashlib
import struct
from ecdsa import VerifyingKey, SECP256k1

class Script:
    def __init__(self, script_sig, script_pub_key):
        self.script_sig = script_sig
        self.script_pub_key = script_pub_key

    def serialize(self):
        # Serialize the ScriptSig and ScriptPubKey with their lengths
        script_sig_len = len(self.script_sig)
        script_pub_key_len = len(self.script_pub_key)
        return struct.pack('B', script_sig_len) + self.script_sig + struct.pack('B', script_pub_key_len) + self.script_pub_key

    @staticmethod
    def parse(data):
        script_sig_len = struct.unpack('B', data[0:1])[0]
        script_sig = data[1:1+script_sig_len]
        offset = 1 + script_sig_len
        script_pub_key_len = struct.unpack('B', data[offset:offset+1])[0]
        script_pub_key = data[offset+1:offset+1+script_pub_key_len]
        return Script(script_sig, script_pub_key)

    def to_json(self):
        return {
            'script_sig': self.script_sig.hex(),
            'script_pub_key': self.script_pub_key.hex()
        }

    def get_message_hash(self, transaction):
        """
        Compute the message hash for a P2PKH transaction. It takes the full transaction in binary format and doublesSHA256 it
        """
        # Serialize the transaction
        serialized_transaction = transaction.serialize()

        # Compute double SHA-256
        first_hash = hashlib.sha256(serialized_transaction).digest()
        second_hash = hashlib.sha256(first_hash).digest()

        return second_hash

    def verify_signature(self, message_hash, signature, public_key):
        """
        Verify the signature using the message hash and public key.
        """
        verifying_key = VerifyingKey.from_string(public_key, curve=SECP256k1)
        try:
            verifying_key.verify(signature, message_hash)
            return True
        except Exception:
            return False

    @staticmethod
    def from_transaction(transaction, input_index):
        """
        Extract ScriptSig and ScriptPubKey from a transaction given the input index.
        """
        # Get CoinInput or DomainInput from the transaction
        if input_index < len(transaction.coin_inputs):
            coin_input = transaction.coin_inputs[input_index]
            script_sig = coin_input.script_sig
        else:
            coin_input = None
            script_sig = b''

        # Get ScriptPubKey from the corresponding CoinOutput or DomainOutput
        if input_index < len(transaction.coin_outputs):
            coin_output = transaction.coin_outputs[input_index]
            script_pub_key = coin_output.script_pub_key
        else:
            coin_output = None
            script_pub_key = b''

        return Script(script_sig, script_pub_key)
    def create_p2pkh_scriptpubkey(pubkey_hash):
        """
        Creates a binary ScriptPubKey for a P2PKH output.

        :param pubkey_hash: 20-byte public key hash (as bytes)
        :return: Binary ScriptPubKey
        """
        if len(pubkey_hash) != 20:
            raise ValueError("Public key hash must be 20 bytes long")

        # ScriptPubKey format
        op_dup = bytes([0x76])
        op_hash160 = bytes([0xa9])
        pubkey_hash_length = bytes([0x14])  # 20 bytes
        op_equalverify = bytes([0x88])
        op_checksig = bytes([0xac])
        
        # Construct the ScriptPubKey
        scriptpubkey = (op_dup + op_hash160 + pubkey_hash_length +
                        pubkey_hash + op_equalverify + op_checksig)
        
        return scriptpubkey

