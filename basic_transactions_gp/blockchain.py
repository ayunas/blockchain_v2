# Paste your version of blockchain.py from the client_mining_p
# folder here
import sys
sys.path.append("..")

from Blockchain import Blockchain

class Transactions(Blockchain):
    def __init__(self):
        super().__init__()
    
    def new_transaction(self,sender,receiver,amount):
        tx = {'sender' : sender, 'receiver' : receiver, 'amount' : amount}
        print(self.current_transactions)
        self.current_transactions.append(tx)



t = Transactions()

t.new_transaction('amir','mom',20)

nonce = t.proof_of_work(t.last_block)
t.new_block(nonce)

print(t.chain)

