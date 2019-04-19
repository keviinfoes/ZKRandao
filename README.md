# ZKRandao
A randao implementation for RNG (random number generator). ZK-snarks are used in the RNG proces, the ZK-snarks are NOT used for anonymity.

# Other randao implementations
Randao is an implementation of a RNG generator, as the name shows it is implemented as DAO on a blockchain. 
- The classic RANDAO contains the following logic:
    1. collecting valid sha3(s). Everyone in the network can send a sha3(s).
    2. collecting valid s.
    3. calculating a random number, refund pledged ETH and bonus.
This implementation of RANDAO is biasable, becasue each proposer can bias the entropy by one bit through the choice of not revealing their pre-committed entropy. 

- The ETH2.0 implementation of RANDAO, refer to https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980.
In this implementation a validator commits to the innermost value in a hash onion. Every block proposed by a validator the validator peels of a layer of the onion (in other words: include the preimage of the current image). The possible problem here is collusion. Because a validator can share the value and images of the commitment with other nodes. This way other nodes in the network know the value the validator is going to commit and can calculate the new state of the blockchain and/or other users of the random number in advance. 

# Description of ZKRandao
ZKRandao is based on the classic RANDAO implementation, because collusion is mitigated through the fact that everyone in the network can send a sha3(s). This way it wil be unbiased as long as there is one honest participant. The problem with the classic RANDAO is that it is not guaranteed that every participant will reveil the s value. This however can be enforced by using ZK-snarks. 

Enforcing the reveil can by done by the following steps (ZKRandao implementation):
1. collecting valid sha3(s), a predetermined range where s is a value from and the ZK-snark proving that s is within the range.
2. collecting valid s. If the participant that entered the sha3(s) does not include the s (within the limit number of blocks, for example the next block) every node can calculate the value of s and include it. The value of s can be calculated by hashing the range that was included.
3. calculating a random number and sending the reward to the participents. If the reveiler != sender sha3(s) the reward wil be divided between the sender of sha3(s) and the reveiler. 

Based on this implementation every participant is incentivized to participate and to reveal the valid s within a limit of blocks and the reveil of s is certain.
