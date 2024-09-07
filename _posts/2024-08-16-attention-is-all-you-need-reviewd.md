---
layout: post
title: "'Attention is all you need' Reviewed" 
date:   2024-08-16 12:00:00 +0100
categories: blog research llms 
short_intro: "Review of transformers paper"
highlights:
    -
    -
    -
---

The paper propose the simplification of NN for translating tasks, allowing 
a bigger model to be trained in less time.
Classic architectures for translating tasks are based in Recurrent Neural 
Networks (RNN) and Convolutional Neural Networks (ConvNN), usually with a 
global attention layer. 

Convolutions makes harder to keep attention in larger sequences between 
distant sequence's positions. The proposal of a multi-headed attention breaks 
the attention mechanism into smaller parts that can be trained in parallel and 
learn different aspects of language (syntatic structures and semantics). 
Furthermore, the model is more interpretable, being able to visualize 
graphically how vectors relate to each other
