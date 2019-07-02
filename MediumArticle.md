ZK RANDAO 

This is a short thought experiment on a new type of RNG (random number generator), based on the randao implementation. Randao is a DAO (decentralized autonomous organization) that uses a commit and reveal scheme to generate random numbers. The ZKRandao implementation of randao uses ZK-snarks to eliminate the attack of not revealing the pre-committed hash. Note that the ZK-snarks are NOT used for anonymity.
Commit and reveal theme
The commit and reveal scheme in ZKRandao can be divided in two options:
Single secret calculation.
Batched secret calculation
Single secret calculation
Collecting a valid sha3(s), a range S where s is part of S and a ZK-snark proving that s for sha3(s) is within the range S.
Reveal s for sha3(s). This can be done by the initiator in step 1 or by other participants (with a preset delay). Other participants can calculate sha3(S) by calculating the hash for the values in range S and comparing these to the sha3(s).
Batched secret calculation
Collecting valid sha3(s), a range S where s is part of S and a ZK-snark proving that s for sha3(s) is within the range S.
Reveal s for sha3(s). This can be done by the initiator in step 1 or by other participants (with a preset delay). Other participants can calculate sha3(S) by calculating the hash for the values in range S and comparing these to the sha3(s).
Calculating a random number based on the collected s values and sending the reward to the participents (initiators and reveilers). Note that based on step 2 it is possible that the initiator != reveiler.
The benefit of the batched model is that there can be more participants, but it has more complexity and therefore possibly more attack vectors. Both models of the ZKRandao scheme preserve the benefit of randao where one honest participant is enough to generate a random number and eliminates the risk of no reveal. Because the range of the secret (s) is shared it is possible to calculate the secret. Every participant is therefore incentivized to participate and reveal, else the reveal will be done by another participant (calculator).
Considerations single RNG
In the considerations we will focus on the simple single secret calculation model.
Sharing ranges eliminates the risk of no reveal, however it generates the risk of other participants calculating the secret (random) number before the number is revealed. Boundaries can be set for this, based on the range and hashrate of calculators. Therefore it is necessary to find the optimal range where it is viable for other participants to calculate s within a maximum set timeframe but not before a minimum set timeframe. Below we will have a short example evaluation of the boundaries. These are simplified because it is a thought experiment. In the calculations the following symbols are used:
R = Range provided by participants
Hr = Hashrate per second of participants 
Ts = Time in seconds for secrect calculation 
Time calculation single secret
(R / 2) / Hr = Ts
This is the time needed to calculate the secret of one shared sha3(s). The range is divided by 2 because of the assumption that the secret will be evenly distributed over the range of the population of participants. For a significantly large population this can be simplified to the fact that the secret will be found at around half of the range.
Evaluation of boundaries
We use the pooled hashrate of Bitcoin, around 62,500,000 Th/s, to calculate the range for a minimum time needed to calculate a secret in this example 62,500,000,000,000,000,000 * 2 * 180 = 22,500,000,000,000,000,000,000.
For the maximum time needed we expect a pooled hashrates of 14,000 Th/s. These are around 1,000 Bitmain Antminer S9i (14 Th/s each). The time needed is (22,500,000,000,000,000,000,000 / 2) / 14,000,000,000,000,000 = 535,715 seconds. Around 9 minutes. At a cost of around 1,000 dollar the cost of mining equipement in this pool is 1 million dollar. With this example the random number can be expected to be fair within a reveal of 180 seconds. If there is one reveal by the initiator within 180 seconds (in a population of multiple random numbers) that number can be expected to be fully random, with the assumption of the maximum hashrate of the pooled bitcoin network (which is significant).
You can play around with the hashrate (minimum and maximum), time needed and ranges to optimize the boundaries. Further note that the bitcoin mining pool is not incentivized to calculate the random number because the initiator is preferred to reveal and therefore no reward will be expected. For example if the initiator reveals after the reveal by a calculator (within a timeframe) the reward will go to the initiator. This will limit the hashrate that is used for calculating the secrets.
Conclusion
The ZKRandao implementation uses adjustable boundaries to create a RNG that is optimized between liveness and integrity of randomness. The most important considerations in ZKRandao are the range and the expected hashrates. By choosing a (relative) small range the liveness assumption is given more weight in exchange for less integrity of the randomness. By choosing a big range the liveness assumption is given less weight in exchange for higher integrity of the randomness. Further the users of ZKRandao can choose the number of secrets (or minimum number of secrets with < 180 second reveals) that are needed for the random number calculation. One ZKRandao RNG can therefore be used by different users with different liveness and integrity of randomness assumptions.
Note that the random number is not directly manipulated when the secret is calculated, the secret is only known by the calculator. To manipulate the random number, all random numbers of a set (determined by the user of the RNG) need to be known by the calculator and the last secrets of that set needs to be initiated by the calculator. This is much harder.
