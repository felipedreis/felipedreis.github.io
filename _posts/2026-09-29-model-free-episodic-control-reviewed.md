---
layout: post
title: "'Model-Free Episodic Control' Reviewed" 
date:   2026-09-29 12:00:00 +0100
categories: blog research episodic-memory
short_intro: "review of Model-Free Episodic Control"
highlights:
    - This paper propose the Model-Free Episodic Controller, that stores episodes and
        and q-scores, and decides which action to take based on the max score  
    - The authors execute their algorithm in the Atari benchmark and Labyrinth simulation
        environment
    - MFEC achieves greater learning performance, even in environments where 
        episodes rarely repeat
---

In this paper the authors compare an episodic controller implementation with DQN and A3C in two
different benchmarks, the Atari and Labyrinth. In Atari they also compare against DQN with
prioritised replay; in Labyrinth the only baseline is A3C.

Citing Daw, Niv & Dayan (2005), the authors note that when an accurate
model of the environment is available and there's enough time and working memory available, the
best approach to control is model-based planning. Their point is that early in a new environment
neither the model nor the slow model-free learner is accurate yet, and this is where episodic
control is most useful. They also point out that episodic control could be seen as limited in
complex environments due to rarely repeating states, but what they observe is that even in a 3D
environment the episodic control still performs well. Atari states repeat 10–60% of the time, while
in Labyrinth fewer than 0.1% of states are exact matches.

They represent the episodic memory as a table \\(Q^{EC}(s, a)\\) where each entry contains the
highest return ever obtained by taking action a from state s. In practice this is one buffer per
action. At the end of each episode, the table is updated according to the return received from the
actions, setting it to the max between the previous value and the returned. To avoid the table
growing indefinitely they apply an LRU forgetting policy. States are obtained from the observations
via an embedding function. To address novelty, the states are imbued with a metric (Euclidean
distance in the embedding space), and the k-nearest states are selected, and the score of an unknown
(state, action) pair is calculated by averaging these KNN. This averaging only happens when there is
no exact match; if (s, a) is already in the table, its stored value is used directly. At each step
the action that maximizes the estimated \((\hat{Q}^{EC}\\), i.e. the best return previously
observed, is selected. At the end of the episode they update the \\(Q^{EC}\\) table in a backward
pass, from t = T down to 1, computing the discounted return at each step so that every state-action
pair in the episode receives the full return of the sequence it led to in a single sweep. They argue
this backward pass is a possible algorithmic version of hippocampal reverse replay (Foster & Wilson,
2006). After a rat reaches a reward, the place cells along its path reactivate in reverse order,
linking the reward to every location on the route. The authors note this link is still an untested
hypothesis.

They say that the score in the table does not correspond to estimates of expected return, but to the
estimate of the highest potential return for a given state-action pair. And behaving according to
this value is useful in regimes where exploitation is more important than exploration 
and where the environment has little noise.
The max operator keeps the best outcome ever seen and never lowers it. In a deterministic
environment that outcome can be repeated, so latching onto it is correct. In a stochastic
environment the agent would chase lucky outcomes and could never unlearn them, which the authors
call risk-seeking behaviour. Storing \\(R_t\\) without the max was tried and performed worse.
The table starts empty and there is no separate training phase for the controller.
Learning is online, episode by episode. Early behaviour is close to random until the first reward is
written into the table. Only the VAE is pre-trained, on 1M frames from a random policy, and those
curves are shifted by 1M frames to account for it.

They tested their algorithm in two environments, Atari and Labyrinth. For each environment they
tested two embedding functions: 64 random projections of the pixels, and the 64 parameters (32 means + 32
log-standard-deviations) of the VAE's Gaussian posterior over its latent dimensions. They state
that exploration was achieved by an \\( \epsilon \\)-greedy policy with epsilon equal to 0.005 (a per-step
probability of taking a uniformly random action, roughly 1 in 200 decisions, apparently kept fixed
with no decay schedule), and that higher exploration rates were not beneficial because more
exploration makes exploiting what is known harder. Because of the max
update, exploratory episodes can't lower the stored values, so the memory isn't diluted. The real
cost is that a random action partway through an episode knocks the agent off a trajectory whose
value depends on an exact sequence of actions, wasting the rest of the episode. The result is less
obvious than it seems, since DQN and A3C use rates at least 10x higher and usually suffer when
\\(\epsilon\\) is cut that much. 

The episodic controller outperformed other algorithms during the initial learning
phase for all games, but it was eventually overtaken on Q\*bert and River Raid. 
The embeddings made little difference in Atari, except in Frostbite, where the VAE was worse. 
In Labyrinth the VAE clearly beat random projections, and increasing k improved results, 
which is evidence that the learned embedding lets
the controller generalize across states that never repeat. In Forage,
eventually A3C caught up with the episodic controller and surpassed it, but the episodic
controller was still more efficient in number of samples early on. In Forage & Avoid, A3C needed
over 40M frames to reach what EC reached in under 3M. In Double T-Maze, A3C never got above zero
expected reward, while EC-VAE learned a positive policy after 20–30M frames. This sparse-reward case
is where one-shot memorisation helps the most.

