---
layout: post
title:  "Reproducing Episodic Control Papers' Results on Snake"
date:   2026-10-07 12:00:00 +0100
categories: blog research reinforcement-learning 
short_intro: ""
highlights:
    - Will fill later 
---

- Action selection in an environment 
  - how agents interact with their environments
    - agents perform actions that change the environment
    - the 
  - how they select actions
  - reinforcement learning
    
- Model-free and Model-based control
  - model-based is when I have an internal simulation/predictor model that gives me the ability to
  - model-free is when I have a kind of heuristic based on experience that helps me decide which action I should take given the current state/perception.
  - life-forms endowed with simpler nervous systems explore a lot of model-free action selection, which is explained by conditioning and simple associative-episodic memory
  - An episodic memory is an n-tuple of the observation/state/reward 
- Episodic Control
  - Model-free episodic control (MFEC) works by storing the episodes, grouped by action, keyed by the perception embedding together with their outcomes
  - A metric in the embedding space is implied
  - the algorithm pulls, for an action, the corresponding embeddings 
- Reproducing the results in a snake game
