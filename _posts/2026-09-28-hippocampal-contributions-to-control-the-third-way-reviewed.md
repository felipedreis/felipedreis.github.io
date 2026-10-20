---
layout: post
title: "'Hippocampal Contributions to Control: The Third Way' Reviewed" 
date:   2026-09-28 12:00:00 +0100
categories: blog research episodic-memory
short_intro: "review of hyppocampal contributions to control"
highlights:
    - Authors compare an implementation of episodic controller against a model-based
        controller in a Markov Decision Process 
    - They claim episodic control beats model-based control after substantial experience 
    
---

The author discusses three control strategies:

* model free (habitual, attributed to the dorsolateral striatum; taken from Daw et al. 2005 and not
  analyzed in this paper)
* model-based (identified with semantic memory and prefrontal cortex)
* and the one introduced by the paper, which is episodic control (attributed to the hippocampus and
  medial temporal cortex)

The paper's own analysis compares only model-based and episodic control.
The example of model-free he gives is Q-learning, which is fast at deciding but slow in learning,
requiring many samples, because it learns by
bootstrapping (value estimates are built from other value estimates, so reward information
propagates backward slowly).

The author explains that model-free control is better than model-based control after substantial
experience because it is more accurate at that point.
Model-based control must search a decision tree, and the approximations this requires (pruning,
sub-sampling) introduce computational noise. Model-free control just looks up cached values, so it
has no computational noise; once enough experience has reduced its statistical error, it wins. And
episodic control is better than model-based control after just a few experiences of the agent (with
little data, all actions look almost equally valuable, so even small computational noise flips their
ranking; episodic control does no search and has no such noise).

The authors propose to analyse the trade-offs when choosing actions that maximize long-term rewards
in sequential decision-making problems. The process is modelled as a Markov Decision Process
(specifically a tree-structured MDP: no loops, rewards only at terminal leaves, transitions drawn
from a Dirichlet prior; exploration is done separately by a "parallel sampler" that visits all
state-action pairs uniformly, and controllers are tested on exploitation only).

The main contribution of the paper is a set of analytically and empirically-justified approximations
to the expected return of the model-based
controller, averaged over MDPs drawn from the prior, as a function of the environment's parameters
and the amount of experience. The episodic controller is studied only by simulation.

Its experimental approach is divided in three steps (all three concern the model-based
controller). It calculates the asymptotic performance of the model-based controller when enough
data is collected that the parameters of the MDP are known (this gives a closed-form upper bound).
Then they model the effect of limited experience as noise on the
model-based controller's action values: the true values are scaled down and noise is added, with
both amounts derived from the number of samples. In
the third step, they model limited computational resources (pruning, sub-sampling) using the same
noise form, Q′ = η₁Q + η₂z, but with η₁ and η₂ set by hand. Both noise sources are then combined,
and the episodic controller is compared against this noisy model-based controller in simulation.

Its episodic memory stores sequences of state-actions whenever a reward is high enough. 
"Large enough" means larger than expected a priori, i.e., above the prior
mean reward. An episode is one trial, from its start state to the terminal leaf where the reward
occurs. When several stored sequences pass through the same state, the one with the highest reward
is followed. This is only trivial because of the tree structure; in a continuing environment without
terminal states, episode boundaries and the reference for "better than expected" become real design
questions.

The final claim of the paper is that they show the episodic controller can outperform a model-based
controller, since it doesn't suffer from inaccuracies of
computation, i.e., the noise that comes from approximating an intractable tree search. It does
suffer from statistical inefficiency: it relies on single lucky samples, so its asymptotic
performance is poor. Its advantage holds only with little data, complex environments, and
significant computational noise, and the noise level was chosen arbitrarily.

The author highlights that the challenge lies in the case where exploration and exploitation are
coupled (the case of our architecture dl2l), as the samples become interdependent in a gordian
manner (after the Gordian knot: hopelessly
entangled; the data depends on the policy, which depends on earlier data, so samples are no longer
independent and the analysis becomes intractable). This is presented as a limitation of their
analysis, not of episodic control.

The final remarks place the paper in its context: Daw et al. had just proposed that
model-based and habitual control compete based on their uncertainty, and behavioural data showed
control shifting from hippocampus to striatum during learning. This paper gives a normative reason
for the early hippocampal phase.

It talks about the computational benefit of episodic memory (which
stores particular samples) over semantic memory (which stores distributions). In competitive games,
Nash equilibria are often stochastic, which makes semantic memory seem the natural fit. But
exploiting a real opponent requires remembering exactly how it deviates from those statistics, which
is an episodic task. Food-caching birds are another example: remembering the exact cache site beats
searching all likely places.

It also mentions that building semantic memory
directly from episodic memory, by recalling all similar episodes and averaging them with distance
weights (kernel density estimation, kNN), without any consolidation, is psychologically implausible
due to the priming phenomenon (recalling one episode
makes it more accessible and interferes with similar ones, so humans cannot retrieve many related
episodes in an unbiased way). This constraint applies to brains, not to artificial agents: dl2l
could use kernel-weighted recall over its episodic buffer.
