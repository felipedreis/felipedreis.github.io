---
layout: post
title: "'Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron LM' reviewed"
date:   2025-05-26 12:00:00 +0100
categories: blog 
short_intro: ""
---

Training large language models is a computation intensive task and require 
parallelization for obtaining results in a reasonable time. 
There are different parallelization techniques such as data parallelism, tensor 
parallelization and pipeline parallelization.
Data Parallelism is when the same model is trained with different subsets of the dataset,
Pipeline Parallelism splits the layers over different servers, and Tensor 
Parallelism splits the tensors over different GPUs.

Although the naive usage of such techniques can result in poor training performance 
That said, the authors want to address the question on how to combine parallelization 
techniques to maximize throughput given a batch size without impact on training convergence. 

Authors propose an interleaved pipeline schedule that reduces the pipeline bubble. 
This method increase communication, but the authors propose an optimization that mitigate 
the impact of extra communication.
They also propose an heuristic approach to calculate the microbatch size 
Their model outperforms ZeRO-3 in some cases by 70% (175 and 530 billion parameters).

Authors offers a training schedule that is abble to train 1 trillion parameter 
model in 3 months. Their approach is the first to combine effectively combine 
pipeline and tensor parallelism to train such large model. They also provide a 
few guidelines to combine parallelization techniques and calculate hyperparameters 

Although the paper results are strong, they are very limited to the tested model
and hardware (strong dependency of same intercontects and gpus to get similar performance).
Due to this, the comparison with other parallelisation techniques, such as ZeRO-3, is limited.
This leaves the question of how much of the performance gain comes from the 
techniques and how much comes from the HPC environment?
Its also not clear when the interleaved schedule is a better choice, since the 
authors mention that without scatter/gather, the default schedule performes 
better than the interleaved at larger batch sizes. 

