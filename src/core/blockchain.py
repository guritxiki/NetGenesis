# Blockchain implementation 
from wallet import * 
from block import *
from script import *
from transaction import *

import pickledb

# Load or create the database
db = pickledb.load('example.db', False)

# Set a key-value pair
db.set('username', 'bob')

# Retrieve a value
username = db.get('username')
print(username)  # Output: 'bob'

# Save changes
db.dump()
