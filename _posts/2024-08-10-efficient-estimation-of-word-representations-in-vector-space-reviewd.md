---
title: Efficient Estimation of Word Representations in Vector Space 
---

Based in a simple neural network with one hidden layer, the authors can 
expand the dimensions of vector representations for words, also called 
embbeddings. 
This technique shows an increase of meaning encoded both on spacial directions 
and vectorial subspaces.

By simplifying the neural network architecture, remoing non-linear layers
that was the state of the art at that time, the authors could train bigger 
architectures in higher order vectorial spaces with larger datasets.

The higher-order vectorial spaces encondes semantical and syntatical information,
as well as socio-political-cultural knowledge such as presidents, countries' 
capitals, etc.

This similarities/relationships can be measured using cossine distance. Given
two words A and B, their respective vectors $a$ and $b$, we can calculate
the cossine of the angle between two vectors with the formula:

$\cos(\theta) = \frac{a \cdot b}{\| a \| \| b \|}$

We say both vectors are similar if their cosine distance is close to 1. 
