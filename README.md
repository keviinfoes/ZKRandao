# ZKRandao
A randao implementation for RNG (random number generator). It is NOT anonymous, but ZK-snarks are used in RNG proces.

# Other randao implementations
Randao is an implementation of a RNG generator, as the name shows it is implemented as DAO on a blockchain. 
- The classic RANDAO contains the following logic:
    1. collecting valid sha3(s). Everyone in the network can send a sha3(s).
    2. collecting valid s.
    3. calculating a random number, refund pledged ETH and bonus.
This implementation of RANDAO is biasable, becasue each proposer can bias the entropy by one bit through the choice of not revealing their pre-committed entropy. 

- The ETH2.0 implementation of RANDAO, refer to https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980.
In this implementation a validator commits to the innermost value in a hash onion. Every block proposed by a validator the validator peels of a layer of the onion (include the preimage of the current image). The possible problem here is collusion. Because a validator can share the value and images of the commitment. This way other nodes in the network know the value he is going to commit and therefore can calculate the new state of the blockchain and/or other users of the random number.

# Description of ZKRandao
ZKRandao is based on the classic RANDAO implementation, because collusion is mitigated through the fact that everyone in the network can send a sha3(s). This way one honest participant can create a fully random number. The problem with the classic RANDAO is that it is not guaranteed that every participant will reveil s. This however can be enforced by using ZK-snarks. 

The following steps are included in the ZKRandao implementation
1. collecting valid sha3(s), a range where the value s is in between, the ZK-snark proving that s is in the range.
2. collecting valid s. If the participant that entered the sha3(s) does not include the s (limit in number of blocks, for example in the next block) everyone can calculate the value of s and include it. The value of s can be calculated by hashing the range that was included.
3. calculating a random number and sending bonus to the participents. If the reveiler != sender sha3(s) the bonus wil be divided between the sender of sha3(s) and the reveiler. 

Based on this implementation every participant is incentivized to participate and to reveal the valid s within a limit of blocks. Else someone else will receive the reward for reveiling.
