---
layout: post
title: "'Sailor: Automating Distributed Training over Dynamic, Heterogeneous, and Geo-distributed Clusters' reviewed"
date:   2025-05-04 12:00:00 +0100
categories: blog 
short_intro: ""
---

This paper introduces Sailor, a workload planner and scheduler for machine learning
systems that is capable of efficient scheduling the training in a heterogeneous hardware
multi-zone clusters, achieving a high throughput while keeping the training 
cost under the budget.

In the context of ML training, the throughput can be defined as the iterations per 
second. Cost is the amount of money spent per iteration.  

Heterogeneous hardware in HPC/Cloud environments is the rule 
as the graphic accelerators to train ML workloads have a short lifetime span and 
are frequently upgraded for the newest and more capable models. Most of the 
frameworks are based on the assumption that training will be in a homogeneous 
GPU cluster with inter-node bandwidth. 

The advantage of Sailor is that it can optimize resource allocation with the 
paralellization plan. It consists of a planner, a simulator and a distributed training 
framework. It optimize the resource allocation and parallelization plan for a
user-given objective under constraints. The planner uses the simulator to accuratelly 
model iteration time and memory footprint. The planner algorithm is based on a 
Dynamic Programming search strategy with space prunning. 

The experiment evaluated three aspects of the system: 

- The quality of simulator estimations to memory and iteration 
- Benchmarked the planner against homogeneous and heterogeneous planners available in the literature
- Evaluated how factors such as cluster size, heterogenity and constrainsts affects search time 

The system is evaluated against the planners Piper, AMP, 
Varauna, Aceso in the homogeneus configuration and the planners Metis and
FlashFlex on the heterogeneous case. It's also evaluated against the DTFM in
the geo-distributed case. 

The results show a improvement over the benchmaked dataset and baseline systems. 
Sailor's simulator shows better estimations compared to it's counterparts.
In special estimations for memory footprint (although no deep statistical analysis was conducted). 
It also achieves better throughput in all compared scenarios, while keeping the 
variables under the constraints. Regarding search performance, the types of GPU
looks to drive the algorithm performance. This was not deeply discussed in the paper. 
