# ZKRandao
A randao implementation for RNG (random number generator). ZK-snarks are used in the RNG proces, the ZK-snarks are NOT used for anonymity. This implementation uses the [ZoKrates](https://zokrates.github.io) toolbox with the GM17 back-end for the ZK-snarks. This is a POC implementation and runs on the **testnet Ropsten**. 

*WARNING: zk-snarks need a trusted set-up. The setup was performed on creation of the verifier contract. Because it is a POC no measures where taken to guarantee the destroyal of the toxic waste (the file that can be used to generate false proofs).*

# Description of ZKRandao
ZKRandao is based on the classic RANDAO implementation, everyone in the network can send a sha3(s). This way it will be unbiased as long as there is one honest participant in the set of random numbers selected by the users. The problem with the classic RANDAO is that it is not guaranteed that every participant will reveal the s value. The risk of no reveal to influence the randomness therefore exists. The reveal however can be enforced by using ZK-snarks. 

Enforcing the reveal can by done by the following steps (ZKRandao implementation):
1. collecting valid sha3(s), a predetermined range where s is a value from and the ZK-snark proving that s is within the range.
2. collecting valid s. If the participant that entered the sha3(s) does not include the s (within the limit number of blocks, for example the next block) every node can calculate the value of s and include it. The value of s can be calculated by hashing the range that was included.
3. calculating a random number and sending the reward to the participants. If the revealer != sender sha3(s) the reward will be divided between the sender of sha3(s) and the revealer. 

Based on this implementation every participant is incentivized to participate and to reveal the valid s within a limit of blocks and the reveal of s is certain.

For a more detailed explantation click [here](https://link.medium.com/DNGjptQ5WY).

# Instructions ZKRandao implementation
This repository contains an implementation of ZKRandao. Perform these steps to set up your own ZKRandao node to generate random numbers. This implementation is tested on Ubuntu.

1. Install dependencies:
    - [ZoKrates](https://zokrates.github.io/gettingstarted.html)
    - [Web3.py](https://web3py.readthedocs.io/en/stable/quickstart.html) - `pip3 install web3`
2. Copy this repository.
3. Open the file ZKRandao_node.py and adjust the variables as indicated.
4. Run ZKRandao_node.py.

Enjoy generating random numbers! The reward is 1 ZKR for submit and 1 ZKR for reveal. The ZKR token will be used for the governance of the contract, this includes adjustments in the boundaries for the determination of the random number.

  
