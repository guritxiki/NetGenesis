import struct

class CoinInput:
    def __init__(self, txid, output_index, script_sig):
        self.txid = txid  # 32 bytes (transaction ID)
        self.output_index = output_index  # 4 bytes (output index)
        self.script_sig = script_sig  # Variable length (script signature)
        self.length = 32 + 4 + 1 + len(script_sig)  # Total length of serialized input

    def serialize(self):
        # TXID (32 bytes)
        txid_bin = self.txid
        # Output Index (4 bytes)
        output_index_bin = struct.pack('>I', self.output_index)
        # ScriptSig Length (1 byte)
        script_sig_length_bin = struct.pack('B', len(self.script_sig))
        # ScriptSig (variable length)
        return txid_bin + output_index_bin + script_sig_length_bin + self.script_sig

    @staticmethod
    def parse(data):
        txid = data[:32]
        output_index = struct.unpack('>I', data[32:36])[0]
        script_sig_length = struct.unpack('B', data[36:37])[0]
        script_sig = data[37:37+script_sig_length]
        return CoinInput(txid, output_index, script_sig)

    def to_json(self):
        return {
            'txid': self.txid.hex(),
            'output_index': self.output_index,
            'script_sig': self.script_sig.hex()
        }
class CoinOutput:
    def __init__(self, value, script_pub_key):
        self.value = value  # 8 bytes (value in native coin)
        self.script_pub_key = script_pub_key  # Variable length (script public key)
        self.length = 8 + 1 + len(script_pub_key)  # Total length of serialized output

    def serialize(self):
        # Value (8 bytes)
        value_bin = struct.pack('>Q', self.value)
        # ScriptPubKey Length (1 byte)
        script_pub_key_length_bin = struct.pack('B', len(self.script_pub_key))
        # ScriptPubKey (variable length)
        return value_bin + script_pub_key_length_bin + self.script_pub_key

    @staticmethod
    def parse(data):
        value = struct.unpack('>Q', data[:8])[0]
        script_pub_key_length = struct.unpack('B', data[8:9])[0]
        script_pub_key = data[9:9+script_pub_key_length]
        return CoinOutput(value, script_pub_key)

    def to_json(self):
        return {
            'value': self.value,
            'script_pub_key': self.script_pub_key.hex()
        }
class DomainInput:
    def __init__(self, domain_txid, output_index, script_sig):
        self.domain_txid = domain_txid  # 32 bytes (domain transaction ID)
        self.output_index = output_index  # 4 bytes (output index)
        self.script_sig = script_sig  # Variable length (script signature)
        self.length = 32 + 4 + 1 + len(script_sig)  # Total length of serialized input

    def serialize(self):
        # Domain Transaction ID (32 bytes)
        domain_txid_bin = self.domain_txid
        # Output Index (4 bytes)
        output_index_bin = struct.pack('>I', self.output_index)
        # ScriptSig Length (1 byte)
        script_sig_length_bin = struct.pack('B', len(self.script_sig))
        # ScriptSig (variable length)
        return domain_txid_bin + output_index_bin + script_sig_length_bin + self.script_sig

    @staticmethod
    def parse(data):
        domain_txid = data[:32]
        output_index = struct.unpack('>I', data[32:36])[0]
        script_sig_length = struct.unpack('B', data[36:37])[0]
        script_sig = data[37:37+script_sig_length]
        return DomainInput(domain_txid, output_index, script_sig)

    def to_json(self):
        return {
            'domain_txid': self.domain_txid.hex(),
            'output_index': self.output_index,
            'script_sig': self.script_sig.hex()
        }
class DomainOutput:
    def __init__(self, new_owner_pub_key_hash):
        self.new_owner_pub_key_hash = new_owner_pub_key_hash  # 20 bytes (new owner public key hash)
        self.length = 20 + 1  # Total length of serialized output

    def serialize(self):
        # New Owner Public Key Hash (20 bytes)
        return self.new_owner_pub_key_hash

    @staticmethod
    def parse(data):
        new_owner_pub_key_hash = data[:20]
        return DomainOutput(new_owner_pub_key_hash)

    def to_json(self):
        return {
            'new_owner_pub_key_hash': self.new_owner_pub_key_hash.hex()
        }
class Transaction:
    def __init__(self, tx_type, version, coin_inputs, coin_outputs, lock_time, domain_inputs=None, domain_outputs=None):
        self.tx_type = tx_type  # 1 byte (transaction type)
        self.version = version  # 4 bytes (version)
        self.coin_inputs = coin_inputs  # List of CoinInput objects
        self.coin_outputs = coin_outputs  # List of CoinOutput objects
        self.lock_time = lock_time  # 4 bytes (lock time)
        self.domain_inputs = domain_inputs or []  # List of DomainInput objects (if applicable)
        self.domain_outputs = domain_outputs or []  # List of DomainOutput objects (if applicable)

    def serialize(self):
        # Version (4 bytes)
        version_bin = struct.pack('>I', self.version)
        # Transaction Type (1 byte)
        tx_type_bin = struct.pack('B', self.tx_type)
        # Coin Inputs Count (1 byte)
        coin_input_count_bin = struct.pack('B', len(self.coin_inputs))
        # Coin Inputs (variable length)
        coin_inputs_bin = b''.join(i.serialize() for i in self.coin_inputs)
        # Coin Outputs Count (1 byte)
        coin_output_count_bin = struct.pack('B', len(self.coin_outputs))
        # Coin Outputs (variable length)
        coin_outputs_bin = b''.join(o.serialize() for o in self.coin_outputs)
        # Lock Time (4 bytes)
        lock_time_bin = struct.pack('>I', self.lock_time)
        
        # Domain Inputs (if applicable)
        domain_inputs_bin = b''
        if self.tx_type == 2 or self.tx_type == 3:
            domain_input_count_bin = struct.pack('B', len(self.domain_inputs))
            domain_inputs_bin = b''.join(di.serialize() for di in self.domain_inputs)
        
        # Domain Outputs (if applicable)
        domain_outputs_bin = b''
        if self.tx_type == 2:
            domain_output_count_bin = struct.pack('B', len(self.domain_outputs))
            domain_outputs_bin = b''.join(do.serialize() for do in self.domain_outputs)
        
        # Combine all parts
        return version_bin + tx_type_bin + coin_input_count_bin + coin_inputs_bin + coin_output_count_bin + coin_outputs_bin + lock_time_bin + domain_inputs_bin + domain_outputs_bin

    @staticmethod
    def parse(data):
        offset = 0
        
        # Version (4 bytes)
        version = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        
        # Transaction Type (1 byte)
        tx_type = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        
        # Coin Inputs Count (1 byte)
        coin_input_count = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        coin_inputs = [CoinInput.parse(data[offset:])]
        offset += coin_inputs[0].length
        
        # Coin Outputs Count (1 byte)
        coin_output_count = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        coin_outputs = [CoinOutput.parse(data[offset:])]
        offset += coin_outputs[0].length

        # Lock Time (4 bytes)
        lock_time = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        
        domain_inputs = []
        domain_outputs = []
        if tx_type == 2 or tx_type == 3:
            # Domain Inputs Count (1 byte)
            domain_input_count = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            domain_inputs = [DomainInput.parse(data[offset:])]
            offset += domain_inputs[0].length
        
        if tx_type == 2:
            # Domain Outputs Count (1 byte)
            domain_output_count = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            domain_outputs = [DomainOutput.parse(data[offset:])]
            offset += domain_outputs[0].length
        
        return Transaction(tx_type, version, coin_inputs, coin_outputs, lock_time, domain_inputs, domain_outputs)

    def to_json(self):
        return {
            'type': self.tx_type,
            'version': self.version,
            'coin_inputs': [i.to_json() for i in self.coin_inputs],
            'coin_outputs': [o.to_json() for o in self.coin_outputs],
            'lock_time': self.lock_time,
            'domain_inputs': [di.to_json() for di in self.domain_inputs],
            'domain_outputs': [do.to_json() for do in self.domain_outputs]
        }
    
    
class CoinbaseTransaction:
    def __init__(self, version, outputs, lock_time):
        self.version = version  # 4 bytes (version)
        self.outputs = outputs  # List of CoinOutput or DomainOutput objects
        self.lock_time = lock_time  # 4 bytes (lock time)

    def serialize(self):
        # Version (4 bytes)
        version_bin = struct.pack('>I', self.version)
        # Output Count (1 byte)
        output_count_bin = struct.pack('B', len(self.outputs))
        # Outputs (variable length)
        outputs_bin = b''.join(o.serialize() for o in self.outputs)
        # Lock Time (4 bytes)
        lock_time_bin = struct.pack('>I', self.lock_time)
        
        # Combine all parts
        return version_bin + output_count_bin + outputs_bin + lock_time_bin

    @staticmethod
    def parse(data):
        offset = 0
        
        # Version (4 bytes)
        version = struct.unpack('>I', data[offset:offset+4])[0]
        offset += 4
        
        # Output Count (1 byte)
        output_count = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        
        outputs = []
        for _ in range(output_count):
            # Parse each output
            if data[0] == 1:  # Assuming 1 indicates CoinOutput
                output = CoinOutput.parse(data[offset:])
            else:  # Assuming other values indicate DomainOutput
                output = DomainOutput.parse(data[offset:])
            outputs.append(output)
            offset += output.length
        
        # Lock Time (4 bytes)
        lock_time = struct.unpack('>I', data[offset:offset+4])[0]
        
        return CoinbaseTransaction(version, outputs, lock_time)

    def to_json(self):
        return {
            'version': self.version,
            'outputs': [o.to_json() for o in self.outputs],
            'lock_time': self.lock_time
        }
