---
layout: post
title: "'Attention is all you need' Reviewed" 
date:   2024-08-16 12:00:00 +0100
categories: blog research llms 
short_intro: "Review of transformers paper"
highlights:
    - Introduces a multi-headed attention mechanism that is more parallelizable than the techniques existing before such ConvNN or RNN
    - Different attention blocks seems to learn different grammatical structures, increasing model explainability
    - Experimental results shows relevant improvement for translation tasks
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
graphically how vectors relate to each other. Each attention block seems
to learn a different grammatical structure. 

Not having a short-term memory or a convolution layer to keep track of
sequence ordering, the architecture relies on posional encodings based in 
sin/cos functions. 

Experimental results demonstrate a gain of one order of magnitude in BLEU
(Billingual Evaluation Understudy), a geomtric mean that measures the difference
between the expected text and the resulting machine translation. 
