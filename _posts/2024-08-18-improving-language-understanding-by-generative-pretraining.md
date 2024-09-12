---
layout: post
title: "'Improving Language Understanding by Generative Pre-Training' Reviewed" 
date:   2024-08-18 12:00:00 +0100
categories: blog research llms 
short_intro: "Review of ChatGPT paper"
highlights:
    - Introduces a unsupervised pre-training step on a large text corpus 
    - Fine tune the model in specific-task dataset with small model compositions
    - The model shows an increased performance in many different taks
---

This paper describes in high-level how the authors leveraged a neural network
to generate high quality text in different benchmarks by training it in a unsupervised
step on an large dataset then fine tunning in a task specific dataset. 

The fist step is learning a language model in a large corpus, trying to optimize
the following funciton

$$L_1(U) = \sum_{i} \log P(u_i | u_{i - k}, ..., u_{i - 1}; \theta)$$

where P is the probability of the token \(u_i\) comes after the sequence of 
size \(k\). The probabilities are encoded in the parameters \(\theta\).

The network architecture is composed of twelve layers of multi-headed attention
blocks. As the equations bellow: 

$$ h_0 = U W_e + W_p $$
$$ h_i = transformer(h_{i - 1}) \forall i \in [1,n] $$
$$ P(u) = softmax(h_n W_{e}^{T}) $$

* Where \(U\) is the sequence \(u_{i - k}, ..., u_{i - 1}\)
* \(W_p\) is the position embeddings
* \(W_e\) is the token embeddings 

The paper doesn't give much attention on how the attention block is composed, 
which optimization method it uses or how the network wheights are adjusted. 

During the fine-tuning the network is submited to a supervised step to predict
the label y, given the parameters \(W_y\):

$$P(y|x^1,...,x^m) = softmax(h_l^m W_y)$$

Maximizing the objective:

$$L_2(C) = \sum_{i} \log P(y | x^1,..., x^m)$$

And another objective is given to the algorithm to accelerate convergence,
composing supervised and usupervised objectives together. 
Although the authors don't explain how this accelerate it. 

$$L_3(C) = L_2(C) + \lambda L1(C) $$

With lamda equals to 0.5.

For task specific dataset transformations different combinations of the model
where done, but no explanations on how this affect the training algorithm.

The paper shows how pre-training is relevant for archieving good results, as
the lack of it causes a negative impact of 14% of performance.
