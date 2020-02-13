import hashlib
import json
from time import time
from uuid import uuid4

# from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(proof=0, prev_hash=1)

    def new_block(self, proof, prev_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index" : len(self.chain),
            "timestamp" : time(),
            "transactions": self.current_transactions,
            "proof" : proof,
            # "hash" : prev_hash if not len(self.chain) else self.hash(self.last_block)
            "hash" : prev_hash or self.hash(self.last_block)
        }

        # Reset the current list of transactions
        # Append the chain to the block
        # Return the new block
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        # TODO: Hash this string using sha256
        #encode json string from unicode to utf-8
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        json_block = json.dumps(block, sort_keys=True)
        json_block_encoded = json_block.encode("utf-8") #converts from unicode to utf-8, which is default for encode()
        hash_obj = hashlib.sha256(json_block_encoded) #returns a hash object
        hash = hash_obj.hexdigest()
        # hash = hashlib.sha256(json_block.encode("utf-8")).hexdigest()

        # TODO: Return the hashed block string in hexadecimal format
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block, hard=3):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        # TODO
        json_block = json.dumps(block, sort_keys=True)

        proof = 0
        while self.guess_hash(json_block,proof,hard) == False:
            proof += 1
        
        print('proof', proof)

        print(hashlib.sha256((json_block + str(proof)).encode("utf-8")).hexdigest())

        return proof

    @staticmethod
    def guess_hash(block_string, proof, hard=3):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        zeros = ''
        for i in range(hard):
            zeros += '0'

        guess = f"{block_string}{proof}".encode("utf-8")
        hash_obj = hashlib.sha256(guess)
        hash = hash_obj.hexdigest()

        return True if hash[:hard] == zeros else False

bc = Blockchain()
bc.new_block(20)
print(bc.chain)

bc.proof_of_work(bc.last_block,5)







# # Instantiate our Node
# app = Flask(__name__)

# # Generate a globally unique address for this node
# node_identifier = str(uuid4()).replace('-', '')

# # Instantiate the Blockchain
# blockchain = Blockchain()


# @app.route('/mine', methods=['GET'])
# def mine():
#     # Run the proof of work algorithm to get the next proof

#     # Forge the new Block by adding it to the chain with the proof

#     response = {
#         # TODO: Send a JSON response with the new block
#     }

#     return jsonify(response), 200


# @app.route('/chain', methods=['GET'])
# def full_chain():
#     response = {
#         # TODO: Return the chain and its current length
#     }
#     return jsonify(response), 200


# # Run the program on port 5000
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
