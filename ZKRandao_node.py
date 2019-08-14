#Implementation ZKRandao node

from web3 import Web3
import random
import subprocess
import os

#Set node for Ropsten
web3_ZKRandao = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/a6eaf73151ac4cd386fab484134d4038"))

#Set data for ZKRandao contract
abi_ZKRandao = '''[{"constant":true,"inputs":[],"name":"RevealRangeOther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"Secrets","outputs":[{"name":"secret","type":"uint256"},{"name":"range","type":"uint256"},{"name":"hash1","type":"uint256"},{"name":"hash2","type":"uint256"},{"name":"pending","type":"bool"},{"name":"accountSubmit","type":"address"},{"name":"accountReveal","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NonEmpty","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"indexReaveledSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"indexSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ExpRange","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"RevealedSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"a","type":"uint256[2]"},{"name":"b","type":"uint256[2][2]"},{"name":"c","type":"uint256[2]"},{"name":"input","type":"uint256[4]"}],"name":"submitRN","outputs":[{"name":"r","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"a","type":"uint256[2]"},{"name":"b","type":"uint256[2][2]"},{"name":"c","type":"uint256[2]"},{"name":"input","type":"uint256[8]"},{"name":"blocknumber","type":"uint256"}],"name":"revealRN","outputs":[{"name":"r","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"RevealRangeSubmitter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"CheckHash","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"Blocknumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"s","type":"string"}],"name":"Verified","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"secret","type":"uint256"}],"name":"SecretShared","type":"event"}]'''
address_ZKRandao = web3_ZKRandao.toChecksumAddress("0x3D6A7061Bb4F3dDd33cBfeaE24dc72167aE51281")
contract_ZKRandao = web3_ZKRandao.eth.contract(address_ZKRandao, abi=abi_ZKRandao)

#Set blocknumber counter
indexBlockNumber = web3_ZKRandao.eth.blockNumber

#Set boundaries based on ZKRandao contract
ExpectedRange = contract_ZKRandao.functions.ExpRange().call()
RevealRangeSubmitter = contract_ZKRandao.functions.RevealRangeSubmitter().call()
RevealRangeOther = contract_ZKRandao.functions.RevealRangeOther().call()
print("ZKRandao Range: {}".format(ExpectedRange))
print("ZKRandao blocks between submit/reveal submitter: {}".format(RevealRangeSubmitter))
print("ZKRandao blocks between submit/reveal others: {}".format(RevealRangeOther))

#Context manager for changing the current working directory
class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# Async functions for reading the chain
def handle_event(block_filter):
    if block_filter != None:
        print("New Block Ropsten: {}".format(block_filter.number))

        #Generate random number = secret
        Secret = random.randint(1, 1001)
        print("New Secret: {}".format(Secret))

        #Input secret number in ZoKrates for hash calculation
                #Adjust the below path to the ZKRandao.code file
        with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao0.1/ZKRandao_hash"):
                #Adjust the below path to the zokrates executable file
                subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "compute-witness", "-a", "0", "0", "0", str(Secret)], stdout=subprocess.DEVNULL)

                # Save the hash variables
                process_out1 = subprocess.Popen(["grep", "~out_1", "witness"], stdout=subprocess.PIPE)
                process_out0 = subprocess.Popen(["grep", "~out_0", "witness"], stdout=subprocess.PIPE)
                out_1 = process_out1.communicate()[0]
                out_0 = process_out0.communicate()[0]
                # Convert hash variables to string
                out_1 = int(out_1[7:-1])
                out_0 = int(out_0[7:-1])
                print("Hash for secret part 1: {}".format(out_0))
                print("Hash for secret part 2: {}".format(out_1))

        #Run ZoKrates for the submit proof
        Secret_place = ExpectedRange - Secret
        with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao0.1/ZKRandao_submit"):
            subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "compute-witness", "-a", "0", "0", "0", str(Secret),
                           str(out_0), str(out_1), str(ExpectedRange), str(Secret_place)])
            subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "generate-proof"])

        
        
## TO DO - ADD REVEAL CHECK SUBMIT AND THEN REVEAL AFTER X BLOCKS
        
        
        #Run ZoKrates for the reveal proof
        with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao0.1/ZKRandao_reveal"):
            subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "compute-witness", "-a", "0", "0", "0", str(Secret),
                            str(out_0), str(out_1), str(ExpectedRange), str(Secret_place)])
            subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "generate-proof"])



def main():
    global indexBlockNumber
    while True:
        TEMPindexBlockNumber = web3_ZKRandao.eth.blockNumber
        if TEMPindexBlockNumber > indexBlockNumber:
            indexBlockNumber += 1
            block_filter = web3_ZKRandao.eth.getBlock(indexBlockNumber)
            handle_event(block_filter)
    else:
        print("Error: Loop terminated")

if __name__ == '__main__':
    main()
