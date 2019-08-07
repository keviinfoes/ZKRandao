# ZKRandao
A randao implementation for RNG (random number generator). ZK-snarks are used in the RNG proces, the ZK-snarks are NOT used for anonymity.

# Description of ZKRandao
ZKRandao is based on the classic RANDAO implementation, everyone in the network can send a sha3(s). This way it wil be unbiased as long as there is one honest participant in the set of random numbers selected by the users. The problem with the classic RANDAO is that it is not guaranteed that every participant will reveil the s value. The risk of no reveal to influence the randomness therefore exists. The reveal however can be enforced by using ZK-snarks. 

Enforcing the reveil can by done by the following steps (ZKRandao implementation):
1. collecting valid sha3(s), a predetermined range where s is a value from and the ZK-snark proving that s is within the range.
2. collecting valid s. If the participant that entered the sha3(s) does not include the s (within the limit number of blocks, for example the next block) every node can calculate the value of s and include it. The value of s can be calculated by hashing the range that was included.
3. calculating a random number and sending the reward to the participents. If the reveiler != sender sha3(s) the reward wil be divided between the sender of sha3(s) and the reveiler. 

Based on this implementation every participant is incentivized to participate and to reveal the valid s within a limit of blocks and the reveil of s is certain.

For a more detailed explantation click [here](https://link.medium.com/DNGjptQ5WY).
