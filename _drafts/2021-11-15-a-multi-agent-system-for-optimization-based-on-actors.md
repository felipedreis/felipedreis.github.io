---
layout: post
title:  "A Multi-Agent System for Optimization Based on Actors"
date:   2021-11-15 12:00:00 +0100
categories: blog research doptimas 
short_intro: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget ligula eu lectus lobortis condimentum. Aliquam nonummy auctor massa."
highlights:
    - Highlight number 1
    - Highlight number 2
    - Highlight number 3
---

Metaheuristics are often used to find suitable solutions to complex optimization problems, where exact methods wouldn't be viable due to time and resources constraints. Regardless of the proven usage of such heuristic and stochastic methods to solve many different problems, there is no general technique that is proven effective in different kinds or families of problems. An alternative to improve the performance of a single method in a broad family of problems is the hybridization of varying search techniques.

Such hybrid strategies that combine ideas of different algorithms or even two or three complete techniques, such as population-based and local search methods, is a practical approach to improving search performance \cite{dokeroglu2019}. However, although the performance of such hybrid algorithms is demonstrably better, this technique does not overcome the same technical disadvantages of problem knowledge and parameter tuning. Quite the opposite, this approach adds more parameters to calibrate.

Furthermore, research into metaheuristics has grown significantly in the last two decades, leading to many different search strategies that make it challenging to manually combine and test their performance on various problems \cite{ser2019}. In addition, hybrid metaheuristics face the theoretical challenges of having a static pattern of interaction and communication, leaving the system unable to adapt to different problems because of the fixed interaction pattern and communication patterns. Therefore, an alternative approach is to use multi-agent systems modelling (MMAS) to promote dynamic hybridization of different search strategies.

An alternative to manually combining two or more search techniques is agent-based modelling, where agents can encapsulate metaheuristics and communicate with each other through message exchange \cite{gong2015, zheng2015}. The latest literature review reports 25 software architectures and frameworks that allow the combination of metaheuristics \cite{silva2018}. Of those 25, agents using agent-based modelling are AgE, CMA, JABAT, MACS, MANGO, and AMAM, each with particular characteristics and different search strategies implemented. 

This paper presents a new optimization architecture called \texttt{d-optimas}, based on the computational actor model \cite{hewitt2013}. Each actor encapsulates a complete agent with a memory component and a metaheuristic capable of communicating with other agents. The search space is organized into regions of interest where agents can collaborate. Metaheuristics are agnostic concerning the implementation of the specific problem, which can be provided at execution time through configuration. The architecture is distributed by design and includes failure tolerance mechanisms such as replication and lead election. 


\textit{Silva et al.} provide a detailed review of the literature presenting 25 software architectures for optimization \cite{silva2018}. The authors divide them into optimization frameworks that use metaheuristics and multi-agent frameworks that use metaheuristics. Additionally, subcategories are established between these two main categories: general and advanced characteristics, multi-agent characteristics, and resources to the optimization process.

This paper aims to develop a multi-agent, distributed, actor-based, and scalable software architecture. In this sense, \texttt{d-optimas} should be compared with similar works in the literature. Of the 25 works presented by\textit{ Silva et al.} (2018), those classified as distributed systems in their advanced characteristics and multi-agent systems were selected. Thus, the following subsections present AgE, CMA, JABAT, MACS, and MANGO architectures with their main features. 

% AgE
AgE (Agent Evolution) is a configurable, component-based platform proposed to solve different optimization problems. The platform uses reusable software components and is based on a mathematical formalism to define an agent-based model \cite{piketak2009functional}. Although various optimization techniques can be used \cite{piketak2013agent}, the only concrete implementation of the framework is based on genetic algorithms and evolutionary multi-agent systems \cite{kisiel2004agent}. Other AgE implementations were found in different languages but without experimental results or demonstrations of the function or advantages of the model.

% CMA
The Collaborative Metaheuristic Algorithm (CMA) is a framework for solving combinatorial optimization problems \cite{malek2009}, consisting of four types of agents: Problem, solution pool, optimizer, and consultant agents. The author presents results for some instances of the traveling salesman problem without a detailed statistical analysis \cite{malek2010}. CMA is designed to collaborate effectively with metaheuristics, encapsulating them into optimizer agents to solve optimization problems.

% JABAT
JABAT is a multi-agent system in which agents collaborate to generate solutions to combinatorial optimization problems. It is based on A-Teams implemented using the JADE library. Proposed by \textit{Jdrzejowicz and Wierzbowska} (2006) and updated by \textit{Barbucha et al.} (2010). It presents two new versions of the architecture: eJABAT, which offers a web interface, and cJABAT, which includes a positive reinforcement learning mechanism \cite{jedrzejowicz2006, barbucha2010}. The architecture solves various problems but is not prepared for solving multiobjective problems.

% MACS
\textit{Martin et al.} \cite{martin2016} proposed a multi-agent cooperative search (MACS) system to solve routing and flow problems. The system uses two types of agents, an initializer and a metaheuristic agent, and communication occurs via a conversation protocol. The results showed that doubling the number of agents in the system significantly improved the search results. The system performed as well as those in the literature without parameter tuning, although it only used two heuristics.

% MANGO
The Multi-Agent Environment for Global Optimization (MANGO) is an architecture based on the JADE platform \cite{kerccelli2008}. Each agent encapsulates a metaheuristic and can communicate with other agents, sharing and requesting solutions or informing about areas of the search space that are suitable for exploration. Communication between agents occurs asynchronously and nondeterministically through message exchange. The architecture implementation is strongly coupled to the optimization problem and only has the Electromagnetism-like Mechanism (EM) heuristic. The author presents only one execution to illustrate the functioning of the architecture without giving a planned experimental procedure.

% AMAM
Finally, the AMAM framework is a multi-agent system consisting of five types of agents responsible for exploring the search space, coordinating communication, and analyzing solutions \cite{silva2007}. The original version of AMAM was later extended with shared adaptive memory, which allows agents to communicate through a shared memory area containing the best solutions found at a given time. The latest version of AMAM abandons the concept of a coordinating agent and instead incorporates a reinforcement learning memory in each agent \cite{fernandes2009}. Results indicate that even with only four cooperating agents, there is a significant difference in the architecture's performance compared to non-cooperating agents. This latest version of AMAM aligns with best practices for modelling multi-agent systems, emphasizing the importance of agent independence \cite{silva2015}.

% LBMAS
