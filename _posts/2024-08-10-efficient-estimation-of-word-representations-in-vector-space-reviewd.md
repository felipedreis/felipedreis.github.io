---
layout: post
title: "'Efficient Estimation of Word Representations in Vector Space' Reviewed" 
date:   2024-08-10 12:00:00 +0100
categories: blog research llms 
short_intro: "review of word2vec first paper"
highlights:
    - Authors trained a simple model over a large dataset to produce word embeddings in a vectorial space 
    - The training produces a set of vectors with linear properties
    - Information is encoded in vector directions and vectorial subspaces 
---

Based in a simple neural network with one hidden layer, the authors can 
expand the dimensions of vector representations for words, also called 
embbeddings. 
This technique shows an increase of meaning encoded both on spacial directions 
and vectorial subspaces.

By simplifying the neural network architecture, removing non-linear layers,
that was the state of the art at that time, the authors could train bigger 
architectures in higher order vectorial spaces with larger datasets. The 
training schema also produces a set of vector that preserves linear properties, 
in a meaningful sense. For example, adding the vectors 
\\(vec("Berlin") - vec("Germany") + vec("France")\\)  results in a vector which its
close neighbor is \\(vec("Paris")\\).

The higher-order vectorial spaces encondes semantical and syntatical information,
as well as socio-political-cultural knowledge such as presidents, countries' 
capitals, etc.

This similarities/relationships can be measured using cossine distance. Given
two words A and B, their respective vectors \\(a\\) and \\(b\\), we can calculate
the cossine of the angle between two vectors with the formula:

$$ \cos(\theta) = \frac{a \cdot b}{\| a \| \| b \|} $$

We say both vectors are similar if their cosine distance is close to 1. 
