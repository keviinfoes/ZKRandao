ZKRandao
This is a short thought experiment on a new type of RNG (random number generator), based on the randao implementation. Randao is a DAO (decentralized autonomous organization) that uses a commit and reveal scheme to generate random numbers. The ZKRandao implementation of randao uses ZK-snarks to eliminate the attack of not revealing the pre-committed hash. Note that the ZK-snarks are NOT used for anonymity. 
Commit and reveal theme
The commit and reveal scheme in ZKRandao can be divided in two options:
Single secret calculation.
Batched secret calculation

Single secret calculation
Collecting valid sha3(s), a range S where s is part of S and a ZK-snark proving that s for sha3(s) is within the range S.
Reveal s for sha3(s). This can be done by the initiator in step 1 or by other participants (with a preset delay). Other participants can calculate sha3(S) by calculating the hash for the values in range S and comparing these to the sha3(s).

Batched secret calculation
Collecting valid sha3(s), a range S where s is part of S and a ZK-snark proving that s for sha3(s) is within the range S.
Reveal s for sha3(s). This can be done by the initiator in step 1 or by other participants (with a preset delay). Other participants can calculate sha3(S) by calculating the hash for the values in range S and comparing these to the sha3(s).
Calculating a random number based on the collected s values and sending the reward to the participents (initiators and reveilers). Note that based on step 2 it is possible that the initiator != reveiler.

The benefit of the batched model is that there can be more participants, but as has more complexity an therefore possibly more attack vectors. Both models of the ZKRandao scheme preserve the benefit of randao where one honest participant is enough to generate a random number and eliminates the risk of no reveal. Because the range of the secret (s) is shared it is possible to calculate the secret. Every participant is therefore incentivized to participate and reveal, else the reveal will be done by another participant. 
Considerations single RNG
In the considerations we will focus on the simple single secret calculation model. 
[ADJUST FROM HERE]
Sharing ranges eliminates the risk of no reveal, however it generates the risk of other participants calculating the secret (random) number before the number is revealed. Boundaries can be set for this, based on the range and hashrate of calculators. Therefore it is necessary to find the optimal range (boundaries) where it is viable for other participants to calculate s within a maximum set timeframe but not before a minimum set timeframe with a expected hashrate.
Below we will have a short evaluation of the boundries. These are simplified because it is a thought experiment. In the calculations the following symbols are used:
R = Range provided by individual participants
Np = Number of participants in one round
Hr = Hashrate per second of participants
Ts = Time in seconds for secrect calculation by one node
Tr = Time in seconds for random number calculation by one node
Minimum time calculation single secret
R / Hr = Ts
This is the time needed by one node to calculate the secret of one shared sha3(s). The time needed needs to be as small as possible to incentivice participants to reveal and for the random numbers to be generated within a fixed timeframe.
Total time calculation random number
R * Np / Hr = Tr
This is the time needed to calculate the random number based on all secrets provided. This needs to be as big as possible so participants cannot calculate the random number within a fixed timeframe.
Evaluation of boundaries
In the ETH2.0 specification one epoch is 6.4 minutes long and one RANDAO reveal happens every epoch. Also a VDF has been defined to be 102 minutes long. The goal is to set a limit that is within the 102 minutes of a VDF for finding the random number, Tr = 102 * 60 = 6,120 seconds. The other goal is that a random number is generated every 6.4 minutes, Ts = 6.4 * 60 = 384 seconds.
Let's expect a hashrate of 1.155 Th/s based on the Bitmain Antminer S5. Calculation of a singe secret is 1,155,000,000,000,000 / 2 * 384 = 443,520,000,000,000,000 [DIVIDE BY 2] 


within this timeframe a range of 443 trillion is needed. Based on the hashrate of  1.155 Th/s and a limit of 102 minutes we can check the minimal number of participants needed. 1.155.000.000.000.000 * 6,120 / 443,520,000,000,000,000 = 16 participants. [ADJUST]
The hashrate needed for one person to calculate the secrets for all of 16 participants in the above example is 443,520,000,000,000,000 * 16 / 384 = 18.480 Th/s. [ADJUST]


Bitcoin currently has a pooled hashrate of around 62,500,000 Th/s. This is significantly higher then 18.480 Th/s. Lets check the minimum number of participants needed based on the pool hashrate of bitcoin 62,500,000,000,000,000,000 * 384 / 443,520,000,000,000,000 = 54,113 participants. [ADJUST]
Note that the financially incentive for calculate the random number can be mitigated by giving a advantage to the initiator in the reveal. For example by preference of the reveal by initiator. If the initiator reveals after the reveal by a calculator (within a timeframe) the reward will go to the initiator. This will limit the hashrate available for calculating the secrets.
Conclusion
The ZKRandao implementation chooses integrity of randomness over liveness. The liveness assumption of the ZKRandao depends on the minimum number of proposers that is set and the number of participants (included hashes and ranges) in one round. The most important consideration in ZKRandao is the range to share. By choosing a (relative) small range the liveness assumption is given more weight in exchange for less integrity of the randomness. By choosing a big range the liveness assumption is given less weight in exchange for higher integrity of the randomness.
Future research 
Attack vector liveness
A possible attack on the liveness would be to send multiple hashes to one round and not reveal. That way the random number is generates after all secrets are found and revealed by calculation. This attack is partly mitigated by the fact that for proposing a hash a zk-snark is needed, which is computation incentive.
