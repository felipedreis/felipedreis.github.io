---
layout: post
title: "'Neural Episodic Control' Reviewed"
date:   2026-10-04 12:00:00 +0100
categories: blog research episodic-memory
short_intro: "review of neural episodic control"
highlights:
    - This paper extends the Episodic Control mechanism with a differentiable
        dictionary, that allows it to fast update keys, while learning an input
        representation through neural network
    - It was compared with MFEC and DQN in the Atari benchmark and achieved 
        faster training with less samples
    
---


In this paper the authors propose a novel episodic control that is differentiable, therefore
trainable by back-propagation (it is the differentiable successor of MFEC, Blundell et al. 2016,
which used a similar per-action episodic table but with a fixed, non-learned embedding). The
hypothesis is that the episodic control reduce the amount of data samples needed to achieve good
performance with deep reinforcement learning. According to the authors, there are three main
problems with DQN:

1. Stochastic gradient descent optimization requires the use of small learning rates (high learning
   rates cause catastrophic interference, so new experience is incorporated only slowly)
2. Environments with sparse reward signal can be difficult for a neural network to model as there
   may be very few instances where the reward is non-zero (a kind of class imbalance, so the
   network under-predicts the rare large rewards)
3. Reward signal propagation by value-bootstrapping techniques, such as Q-learning, results in
   reward information beign propagated one ste at a time thorugh the history of previous
   interactions with the environment (made worse by DQN's random minibatch sampling and its slowly
   updated target network).

All this factors cause the learning of DQN to be very slow and require a lot of data.

To solve this problem the authors propose a semi-tabular representation of the agent's experience of
the environment possessing several of the features of episodic memory such as long term memory,
sequentiality and context-based lookups. The table is append-only and has the property of
context-based lookup on the keys, and the memory values can be updated much faster than the rest of
the DNN. It writes all the agent's experience to memory, and allow it to grow larger compare to
existing memory architectures (up to 5×10⁵ entries per action; when full, the entry least recently
used as a neighbour is overwritten).

Their agent is composed of three parts:

* A convolutional neural network that process the images (the pixel state s) and produces the 
embedding h, which is used as the lookup key,
* a set of memory modules (one per action),
* and a final stage that converts the read-outs into Q-values; in practice the read-out of each DND M_a is
  itself \\(Q(s, a) = \sum{ w_i Q_i} \\), and the agent takes the \\(\epsilon\\)-greedy argmax across actions.

For each possible action, a memory module \\(M_a\\) is a tuple of \\((K_a, V_a)\\), where K and V are arrays
with the same number of entries, where each key hᵢ is an embedding vector and each value \\(Q_i\\) is the scalar
Q-estimate stored for the state that produced that key.

The memory module implements two operations, lookups and writes. The lookup for a key h is a
weighted sum of the values of the p nearest keys, where the weight is
a normalized kernel between h and each
neighbour key, so the weights sum to 1. Closer keys get more
weight, but not in a one/zero fashion: weight scales with the inverse squared distance, so a
neighbour twice as far gets 1/4 of the weight. Only a near-exact match (\\(d << \sqrt{\delta}\\)) dominates;
otherwise it behaves like a soft k-NN interpolation.

For very large memories, they limit the number of neighbour keys to p (p = 50) and use an
approximation via kd-tree to find the neighbours.

They insert all the perceptions/values pairs of the agent interaction lifetime within the
appropriate memory set \\(M_a\\) (the key is h, the value is the N-step return \\(Q^{(N)}\\)). 
A Monte Carlo return is the actual discounted reward received until the episode ends. It
is on-policy, propagates reward instantly, but is noisy. An off-policy backup is the Q-learning
target \\(r + \gamma \max Q(s′, a′)\\), which bootstraps from the agent's own estimate of the best action. It
targets the optimal policy, but is biased and propagates reward one step at a time. The N-step
return mixes both: N = 100 steps of real rewards, then a bootstrap with the max over all DNDs.
Consequently a pair can only be written N steps after it happens. If the exact key already exists,
its value is updated tabularly with a high learning rate \\(\alpha\\): \\(Q_i = Q_i + \alpha (Q^{(N)} − Q_i)\\).

The network parameters are updated by minimising the L2 loss between the predicted Q value for a
given action and the *N-step* estimate on random sampled-mini-batches from a replay buffer. These
gradients update both the CNN weights and the keys and values stored in the DNDs, but with a much
smaller learning rate than the tabular \\(\alpha\\). This two-timescale design (slow keys, fast values) is the
core idea: the agent latches onto good experiences immediately, while the embedding is slowly shaped
so that states with similar values lie close together.

The kernel function to calculate the weights from memory queries is 
\\( k = \frac{1}{||h − h_i||^2  + \delta)} \\), the inverse of the squared distance between the queried key
and the existing in memory  Its heavy tail is deliberate: with a Gaussian kernel, 
all weight would collapse onto the single closest neighbour when every neighbour is far away.

The authors achieved much higher data efficiency (faster early
learning) for most of attari benchmarks used. It is not shown to converge to a better policy: at
40M frames Prioritised Replay beats NEC on the median, and NEC is among the worst on the mean.
Not requiring reward clipping explains its advantage on some
games (Alien, Ms. Pac-Man, Bowling, Frostbite, H.E.R.O.), where clipped agents ignore larger
rewards. However, NEC is also much faster on Pong and Boxing, where clipping changes nothing, and it
beats MFEC, which also doesn't clip. So clipping alone doesn't explain the
speed-up, though its magnitude on clipping-sensitive games is confounded. The stronger critique is
that the paper has no ablations: the gain is attributed jointly to the DND, the N-step returns, and
the stable CNN representation, without separating them.

As for the authors, their work is the first among local-regression (non-parametric) 
value methods to learn the embedding space with the
reward signal, via TD learning (DQN itself already learns its representation from reward). 

The authors result is very strong, but I think the result is cofounded by a few factors that are added 
to the agent's architecture. The paper attributes NEC's speed jointly to three things: 
the episodic memory (the DND), N-step returns, and a stable learned embedding. 
It never tests them separately. When comparing with environments with high rewards,
clipping also affects the result. But NEC also wins on Pong and Boxing (where clipping changes nothing) and against MFEC (which doesn't clip either).
