#Implementation ZKRandao node

from web3 import Web3
import random
import subprocess
import os
import json
import csv

#Set node for Ropsten
web3_ZKRandao = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/a6eaf73151ac4cd386fab484134d4038"))

#Set data for ZKRandao contract
abi_ZKRandao = '''[{"constant":true,"inputs":[],"name":"RevealRangeOther","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"Secrets","outputs":[{"name":"secret","type":"uint256"},{"name":"range_begin","type":"uint256"},{"name":"range_end","type":"uint256"},{"name":"hash1","type":"uint256"},{"name":"hash2","type":"uint256"},{"name":"pending","type":"bool"},{"name":"accountSubmit","type":"address"},{"name":"accountReveal","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NonEmpty","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"a","type":"uint256[2]"},{"name":"b","type":"uint256[2][2]"},{"name":"c","type":"uint256[2]"},{"name":"input","type":"uint256[9]"},{"name":"blocknumber","type":"uint256"}],"name":"revealRN","outputs":[{"name":"r","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"indexReaveledSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"indexSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"ExpRange","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"RevealedSecrets","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"a","type":"uint256[2]"},{"name":"b","type":"uint256[2][2]"},{"name":"c","type":"uint256[2]"},{"name":"input","type":"uint256[5]"}],"name":"submitRN","outputs":[{"name":"r","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"RevealRangeSubmitter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"CheckHash","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"Blocknumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"s","type":"string"}],"name":"Verified","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"secret","type":"uint256"}],"name":"SecretShared","type":"event"}]'''
address_ZKRandao = web3_ZKRandao.toChecksumAddress("0x475126cda76e86bf725d60c96ca0227f10ef9996")
contract_ZKRandao = web3_ZKRandao.eth.contract(address_ZKRandao, abi=abi_ZKRandao)

#Set blocknumber, submit and reveal counter
indexBlockNumber = web3_ZKRandao.eth.blockNumber
indexSubmitRN = 0
indexRevealRN = 0
CurrentSecret = 0
CurrentSecretPlace = 0
BlockCurrentSecret = 0
HashCurrent0 = 0
HashCurrent1 = 0
BeginRangeCurrent = 0

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

#Create CSV file for storing secrets and metadata secrets
Table_namesSubmit = ["blocknumber_submit", "secret", "rangeSecret", "RangeBegin", "hash1", "hash2", "accountSubmit"]
Table_namesReveal = ["blocknumber_reveal", "secret", "rangeSecret", "RangeBegin", "hash1", "hash2", "accountReveal"]

with open('/Users/kevinfoesenek/Desktop/TEST_ZKrandao/DB_SecretsSubmit.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(Table_namesSubmit)
writeFile.close()

with open('/Users/kevinfoesenek/Desktop/TEST_ZKrandao/DB_SecretsReveal.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(Table_namesReveal)
writeFile.close()

# Async functions for reading the chain - submit secret and reveal secret
def handle_event(block_filter):
    global indexSubmitRN
    global indexRevealRN
    global CurrentSecret
    global CurrentSecretPlace
    global BlockCurrentSecret
    global HashCurrent0
    global HashCurrent1
    global BeginRangeCurrent
    if block_filter != None:
        print("New Block Ropsten: {}".format(block_filter.number))
        if indexSubmitRN == indexRevealRN and indexBlockNumber % 5 == 0: #Start submit only every 5 blocks
            #Generate random number = secret
            RangeBegin = random.randint(1, ((ExpectedRange+1)*10**6))
            BeginRangeCurrent = RangeBegin
            Secret = random.randint(RangeBegin, RangeBegin+ExpectedRange+1)
            print("New Secret: {}".format(Secret))

            #Input secret number in ZoKrates for hash calculation
                #Adjust the below path to the ZKRandao.code file
            with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao/ZKRandao_hash"):
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
                    HashCurrent0 = out_0
                    HashCurrent1 = out_1

            #Submit meta data secret on chain
            Secret_place = Secret - RangeBegin
            CurrentSecretPlace = Secret_place
            with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao/ZKRandao_submit"):
                subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "compute-witness", "-a", "0", "0", "0", str(Secret),
                               str(out_0), str(out_1), str(ExpectedRange), str(RangeBegin), str(Secret_place)], stdout=subprocess.DEVNULL)
                subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "generate-proof"], stdout=subprocess.DEVNULL)

                #Create and send submitRN transaction infura
                nonce = web3_ZKRandao.eth.getTransactionCount(web3_ZKRandao.toChecksumAddress("0x4B1366383c1f592Cfe00ab8FB031Fe4D56Ae680e"))

                #Read proof data in json file
                with open("/Users/kevinfoesenek/Desktop/TEST_ZKrandao/ZKRandao_submit/proof.json") as json_file:
                    data = json.load(json_file)
                    data_proof = data['proof']
                    submit_a = data_proof['a']
                    submit_b = data_proof['b']
                    submit_c = data_proof['c']
                    inputs = data['inputs']

                    #Create empty array to add the data
                    a_array = []
                    b_array_total = []
                    b_firsarray = []
                    b_secondarray = []
                    c_array = []
                    inputs_array = []
                    a_array.extend([int(submit_a[0], base=16), int(submit_a[1], base=16)])
                    b_firsarray.extend([int(submit_b[0][0], base=16), int(submit_b[0][1], base=16)])
                    b_secondarray.extend([int(submit_b[1][0], base=16), int(submit_b[1][1], base=16)])
                    b_array_total.extend([b_firsarray, b_secondarray])
                    c_array.extend([int(submit_c[0], base=16), int(submit_c[1], base=16)])
                    inputs_array.extend([int(inputs[0], base=16), int(inputs[1], base=16), int(inputs[2], base=16),
                                         int(inputs[3], base=16), int(inputs[4], base=16)])

                contract_txn = contract_ZKRandao.functions.submitRN(a_array,
                                                                    b_array_total,
                                                                    c_array,
                                                                    inputs_array).buildTransaction({'gas': 999000, 'nonce': nonce})

                private_key = "XXXX"
                signed_txnDeposit = web3_ZKRandao.eth.account.signTransaction(contract_txn, private_key)
                txt_hash = web3_ZKRandao.eth.sendRawTransaction(signed_txnDeposit.rawTransaction)

                #Check transaction succes - received transactionreceipt
                receipt = web3_ZKRandao.eth.waitForTransactionReceipt(txt_hash, 200)
                print("Transactions submit mined")
                print(receipt)
                indexSubmitRN += 1
                CurrentSecret = Secret
                BlockCurrentSecret = receipt.blockNumber

                #Save data submit to csv file
                newRow = []
                newRow.extend([BlockCurrentSecret, Secret, Secret_place, BeginRangeCurrent, HashCurrent0, HashCurrent1, "0x4B1366383c1f592Cfe00ab8FB031Fe4D56Ae680e"])
                with open('/Users/kevinfoesenek/Desktop/TEST_ZKrandao/DB_SecretsSubmit.csv', 'a') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow(newRow)
                writeFile.close()

        #Reveal secret on chain
        if indexSubmitRN > indexRevealRN and block_filter.number - BlockCurrentSecret > RevealRangeSubmitter:
            with cd("/Users/kevinfoesenek/Desktop/TEST_ZKrandao/ZKRandao_reveal"):
                subprocess.run(
                    ["/Users/kevinfoesenek/.zokrates/bin/zokrates", "compute-witness", "-a", "0", "0", "0", str(CurrentSecret),
                     str(HashCurrent0), str(HashCurrent1), str(ExpectedRange), str(BeginRangeCurrent), str(CurrentSecretPlace)], stdout=subprocess.DEVNULL)
                subprocess.run(["/Users/kevinfoesenek/.zokrates/bin/zokrates", "generate-proof"],
                               stdout=subprocess.DEVNULL)

                # Create and send revealRN transaction infura
                nonce = web3_ZKRandao.eth.getTransactionCount(
                    web3_ZKRandao.toChecksumAddress("0x4B1366383c1f592Cfe00ab8FB031Fe4D56Ae680e"))

                # Read proof data in json file
                with open("/Users/kevinfoesenek/Desktop/TEST_ZKrandao/ZKRandao_reveal/proof.json") as json_file:
                    data = json.load(json_file)
                    data_proof = data['proof']
                    submit_a = data_proof['a']
                    submit_b = data_proof['b']
                    submit_c = data_proof['c']
                    inputs = data['inputs']

                    # Create empty array to add the data
                    a_array = []
                    b_array_total = []
                    b_firsarray = []
                    b_secondarray = []
                    c_array = []
                    inputs_array = []
                    a_array.extend([int(submit_a[0], base=16), int(submit_a[1], base=16)])
                    b_firsarray.extend([int(submit_b[0][0], base=16), int(submit_b[0][1], base=16)])
                    b_secondarray.extend([int(submit_b[1][0], base=16), int(submit_b[1][1], base=16)])
                    b_array_total.extend([b_firsarray, b_secondarray])
                    c_array.extend([int(submit_c[0], base=16), int(submit_c[1], base=16)])
                    inputs_array.extend([int(inputs[0], base=16), int(inputs[1], base=16), int(inputs[2], base=16),
                                         int(inputs[3], base=16), int(inputs[4], base=16), int(inputs[5], base=16),
                                         int(inputs[6], base=16), int(inputs[7], base=16), int(inputs[8], base=16)])

                contract_txn = contract_ZKRandao.functions.revealRN(a_array,
                                                                    b_array_total,
                                                                    c_array,
                                                                    inputs_array,
                                                                    BlockCurrentSecret).buildTransaction(
                                                                    {'gas': 999000, 'nonce': nonce})

            private_key = "XXXX"
            signed_txnDeposit = web3_ZKRandao.eth.account.signTransaction(contract_txn, private_key)
            txt_hash = web3_ZKRandao.eth.sendRawTransaction(signed_txnDeposit.rawTransaction)

            # Check transaction succes - received transactionreceipt
            receipt = web3_ZKRandao.eth.waitForTransactionReceipt(txt_hash, 200)
            print("Transactions reveal mined")
            print(receipt)
            print(receipt.blockNumber)
            indexRevealRN += 1

            # Save data reveal to csv file
            newRow = []
            newRow.extend([receipt.blockNumber, CurrentSecret, CurrentSecretPlace, BeginRangeCurrent, HashCurrent0, HashCurrent1,
                           "0x4B1366383c1f592Cfe00ab8FB031Fe4D56Ae680e"])
            with open('/Users/kevinfoesenek/Desktop/TEST_ZKrandao/DB_SecretsReveal.csv', 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(newRow)
            writeFile.close()

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
