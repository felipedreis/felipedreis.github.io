---
layout: post
title:  "Explaining Dynamic PRogramming"
date:   2023-12-08 12:00:00 +0100
categories: blog competitive-programming  
short_intro: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget ligula eu lectus lobortis condimentum. Aliquam nonummy auctor massa."
highlights:
    - Highlight number 1
    - Highlight number 2
    - Highlight number 3
---

My first contact with competitive programming was through dynamic programming. 
I was in a bus, comming back home with a friend who just started univeristy and he was
telling me how excited he was about learning how to solve a problem involving 
items with weights and values assoand a knapsack that was very limited in capacity. I remember he 
teling me how this was just a combinatorial problem and for solving it you
could chose any order and try all possible item combinations.

At first glance, this problem was so silly. I hadn't started uni at that time 
(it took me one semester until I joined computer engineering) and I was focused
on my technical internship, fascinated about frameworks and web programming. Recently
a friend from my previous company who also went through I layoff was studying dynamic
programming for his technical interviews, and I was helping him with the intution.
That remind me of myself 12 years ago on the bus.

The way I started on competitive programming is for another post, for this one 
I want to give a view on how I understood DP, the main intuitions and strategies
on how to solve combinatorial and optimization problems. This post comes from 
a recent invite to talk about my experience with the topic on the competitive 
programming classroom at CEFET-MG. My lecture was split in 4 sections, I started
with a not-very-classical problem but very useful of counting how many different
ways one could climb a staircase using 1 and 2 steps, after that we see how
dynamic programming can be used to solve minimum cost path in a graph, and from 
this problem we can extract valuable intutions. Those intutions could be resumed
in five steps, and we finally apply our learnings on problems, namely edit distance 
and 0-1 knapsack.

# Climbing stairs 

Most of books or tutorials I've used to study starts dynamic programming by 
calculating the n-th term of a fibbonacci sequence. Indeed this problem is very classic,
but it's not very pratical. Although the FB sequence have many usages, I've 
never used it in my day-to-day activities. I prefer to introduce this topic 
with a more pratical, or at least, funny problem.

Imagine you have to climb a start everyday. One day this starts to bore you, and
you decide to make it funnier, trying to alternate 1 and 2 steps. Soon you start to
get bored again. And while climbing the staircase you start to consider how many
different ways one can climb the start alternating one and two steps each time. 

For a simple 2-step staircase, the solution is easy to count. Or you take the 
2 steps one after the other, or you jump them to the last patamar, as in the figure 
below:

[[images/pd/example1.png]]

As you can see, for `n=2`, `C(n)=2`, and you can do the same math for other 
saircase sizes, like 3 and 4 and summarize our results. This can give us a good 
intuition on where the results are going:

```
C(1) = 1
C(2) = 2
C(3) = 3
C(4) = 5
```
But this don't solve our problem yet. If you enumerate the cases, anddraw 
them, you can see similarities between the solutions. In special, for a N=4, 
I chose two solutions that are prety similar, as you can see in figure
