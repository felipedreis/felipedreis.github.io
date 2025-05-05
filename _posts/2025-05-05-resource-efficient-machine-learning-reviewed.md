---
layout: post
title: "'Resource-Efficient Machine Learning' reviewed"
date:   2025-05-04 12:00:00 +0100
categories: blog 
short_intro: ""
---

The document resumes the discussions from the Dagsthul Seminar 24311. It happened
in 4 working groups: 
 
    1. Resource-Efficient Data Selection;
    2. The Future of Portable, Extensible and Composable Machine Learning Systems
    3. Hardware-Software Co-Design for Machine Learning 
    4. Workload-Aware Machine Learning Serving 

Regarding the topic 4, it highlights that model personalization, fine tunning and 
prompt engineering is a growing trend, while weight prunning and saprsity exploitation
is becomming more practical. Although most of the existing tools are applied in
a heuristic manner, in isolation, and/or in a pre-deployment phase. 

The authors point to  an opportunity to design an algorithm that adaptively tune these optimization
variables on a per-request basis, in an online optimization fashion. 

With that, they envision that it would be possible to deploy multiple variants
of sparsified and specialized models .
Periodically profile samples of client requests, and then tune the deployment 
configurations to maximize throughput subject to accuracy, energy and latency constraints. 

The methodology proposed encompass:

    1. share a workload characterization of real serving traces, the potential of sparsification and oportunities of adaption.
    2. Develop a reconfiguration system with an optimization method, tuning hyperparameters and objectives
    3. Conduct preliminar experiments on two different prototypes for LLMs and traditional ML models 

