import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(proof=0, prev_hash='lambda')

    def new_block(self, proof, prev_hash=None):
        block = {
            "index" : len(self.chain),
            "timestamp" : time(),
            "transactions": self.current_transactions,
            "proof" : proof,
            # "hash" : prev_hash if not len(self.chain) else self.hash(self.last_block)
            "hash" : prev_hash or self.hash(self.last_block)
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        json_block = json.dumps(block, sort_keys=True)
        hash = hashlib.sha256(json_block.encode("utf-8")).hexdigest()
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block, hard=3):
        json_block = json.dumps(block, sort_keys=True)

        proof = 0
        while self.guess_hash(json_block,proof,hard) == False:
            proof += 1

        return proof

    @staticmethod
    def guess_hash(block_string, proof, hard=3):
        zeros = ''
        for i in range(hard):
            zeros += '0'

        guess = f"{block_string}{proof}".encode("utf-8")
        hash_obj = hashlib.sha256(guess)
        hash = hash_obj.hexdigest()

        return True if hash[:hard] == zeros else False