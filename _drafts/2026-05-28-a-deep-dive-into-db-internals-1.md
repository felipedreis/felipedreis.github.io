---
layout: post
title:  "A Deep Dive into Database Internals - Part I - How B-Trees Work"
date:   2026-05-28 12:00:00 +0100
categories: blog learning databases
short_intro: ""
highlights:
    - After 15 years of using databases, I realized I didn't actually know how they work — and that bothered me enough to do something about it.
    - Learning by doing — building a B-Tree key/value store from scratch in Go, because reading a book isn't the same as "show me the code".
    - Disks read and write in 4KB blocks, not bytes, and that single constraint is why binary search trees give way to B-Trees once data leaves memory.
--- 

# Isn't a text file enough? 

When I started programming 15 years ago I was always wandered on 
how data is actually stored for real-life systems. I remmber when I learned
how to read files with C/C++ for the first time int Technical High School.
What a mess was to store  different types of records (structs) for a single application.
The final assignment for the programming course was to build a simple manager for 
client contacts or something like that. 
I think what I did was to write in plain text, serialize records into a string, 
using a separator character per field and write one record per line.
I didn't know at the time, but this is called CSV.
This works fine until you have to erase records. How do you do that? Write a state
at the end of the line, and then you have a tombstone mark. From time to time
you read and rewrite your file to remove tombstones.

And then you learn how to use databases and everything becomes magic.
You learn a little bit of SQL, how to create tables, how to insert data, how to 
query, join and filter your data, and how to chage it inside a transaction
and everything is in a consistent state at the end. 
And suddenly you forget that storing and managing data was a problem. 
You treat your favorite DBMS as your infinite data ATM where you can withdraw 
data with minimal performance costs. 
If you really grow on scale and the classic relational DBMS starts to move slowly
you've heard about NO-SQL and how it's blazingly fast, and much more flexible than
relational.
You decide to make the change, just to hit the same wall some time latter:

# You don't understand how databases works. 

I didn't. And don't get me wrong, I know how to write SQL. 
I know how to model data in relational and non-relational DBMS.
I know joins are expensive. 
I know the query planer sometimes can be tricky to you.
I've worked with databases for the last 15 years, but the shameful truth is that
I don't know how do they work. 

Maybe this is not just me. 
Maybe all software engineers come to this obscure moment in their career that 
they feel like a fraud, like I was feeling. 
I took databases for granted, that they were there to solve my performance problems,
and for some kinds of problems, I would chose this or that technology.
Like a Redis/Memcached for caching, a datawarehouse for analytics, a relational
database for the heavy-duty reliable source. 
But no, this was not enough. I had to deep dive into how they actually work.

A lot of colleagues recommended me to read the "Designing Data Intensive Applications". 
I actually bought the book, but it's still not the one I'm talking about today.
I wanted something deeper and I found the "Database Internals", by Alex Petrov.
Reading the book you get a very good picture of what is behind the storage of your data: 
The B-Tree data structure. 
This is where all the magic becomes code, and a good storage engine depends a 
lot on the decisions the engineer puts in the B-Tree implementation. 
Different from other data structures that I studdied during undergrad, you really
have a lot of different implementation alternatives and small optimizations 
in a B-Tree that makes it deserve a book for itself. 

But reading the book is not enough for me. 
During undergrad I was competing in ICPC regionals, and I implemented a lot of 
data structures and algorithms. 
I learnt how to learn by doing. 
For me it only make sense if you "shut up and show me the code".

{% include figure.html src="/images/show-me-the-code.webp" alt="Shut up and show me the code" caption="The universal mantra of every engineer who learns by doing." %}

It's shameful that we didn't implement during undergrad a simple B-Tree Key/Value store.
So I decided this was the time, to give it a try and implement it. 
This article, and probably two or three next ones will resume my learnings on the
B-Tree implementation. 
I come from a long journey with Java, but for this project I decided to do it in
Golang, because first, I already see Java code for 8h/day, 5 days/week. 
If I'm coding on my free time, to be at least with something different. 
Second, since I'm learning one thing, why not learn two. 
Third, I've been looking with curiosity into Go for a while, it seems super simple,
but at same time incredibly powerful. 

A little disclaimer before we start to talk about the real thing. 
For this project in special I tried to not use AI at the begining. 
In the end, my intention is engaging in learning.
If I ask Claude or Gemini to generate a B-Tree implementation for me, it will 
do it in seconds.
I could read it, pretend I understand something and go back to live my life, 
with my curiosity satisfied. 
So the initial intention was not to use AI at all, but then I got myself googling 
all the fundamental Golang stuff that I know by hearth in Java and I felt stupid.
So I gave up, and started using the AI as a tutor. 
That was actually very helpful and I could write something about later.

And now, let's cut the chase and go up to the tree, or better, go down. 

# What is actually a B-Tree

If you are still here, you're probably familiarized with the concept of a [Binary
Search Tree](https://www.geeksforgeeks.org/dsa/binary-search-tree-data-structure/),
in which we store ordered keys in a clever way that I can look for
them in `O(lg N)` time. 
We achieve this with a structure where every key points to two other elements,
on the left sits all the elements that are less than a key, and to the right 
all the elements that are grather then the key. 

This structure is very efficient to store and search for data in memory, where
one can randomly access memory addresses in `O(1)`. 
But disks don't work that way.
Inside a Hard Drive or an SSD data is stored in blocks of 4Kb or multiples of 
it, and we only read/write the disk in multiples of this block size. 

{% include figure.html src="/images/b+tree.svg" 
    alt="Binary Search Tree and A B+Tree on the right" 
    caption="A binary search tree start growing from the root. Every node has 
        two pointers, on to the left side where all keys are smaller then the current node
        and one to the right where all the nodes are greater than the current node. 
        A B-Tree is a generalization of a BST, where every node have K keys and 
        K+1 child. In our particular case, we are implementing a B+Tree where 
        only leaf nodes store values. The leaf nodes have K key/value pairs. 
        Non-Leaf nodes are called Internal Nodes. The keys are kept sorted 
        to allow us binary-search on them." %}

Given that constrain in mind, it makes some sense that, if we want to save data 
to the disk in the same clever way that allows us to search quickly for a key,
it would be nice if we could pack as much keys inside a node as possible.
This way, we can view a BT as a generalization of a BST, where every node has 
`K` keys and `K+1` pointers to child nodes, except for leaf nodes who only have
`K` key/value pairs. 
Every key still conserves two search directions, a left one that points to all elements 
that are smaller than the key, and the right points for all the elements that 
are greater than or equal to it. 

I won't give all the theoretical details and variants of B-Tress (the specific
one I chose to implement was a B+Tree, in which only leaf nodes keep values). 
For that you can refer to the book. 
What I'll do here is talk about the concepts that probably are well covered 
in the book as well, but only clicked to me when implementing it. 


The first idea is that, different from a BST that grows from the root to the 
leafs, a BT grows from the leaf up to the root node. 
In other words, when you start a fresh BT, you have an empty leaf node, and you
insert keys on it until you reach that node maximum capacity.
When you reach that maximum capacity, you have to do something, and it's now that
your data structure starts resambling a tree. 
The more logical thing to do is split your keys into two nodes, and create a 
parent for it, preserving the tree invariant. 
Because of the way the tree grows, all it's leafs will always have the same hight. 
Regarding the node capacity, most of the textbooks I read establish capacity based on
the number of keys. 

{% include figure.html src="/images/b+tree-insertion.svg" 
    alt="Binary Search Tree and A B+Tree on the right" 
    caption="A binary search tree start growing from the root. Every node has 
        two pointers, on to the left side where all keys are smaller then the current node
        and one to the right where all the nodes are greater than the current node. 
        A B-Tree is a generalization of a BST, where every node have K keys and 
        K+1 child. In our particular case, we are implementing a B+Tree where 
        only leaf nodes store values. The leaf nodes have K key/value pairs. 
        Non-Leaf nodes are called Internal Nodes. The keys are kept sorted 
        to allow us binary-search on them." %}

So, from this perspective, we already know how an empty tree grows from one node
to several, and we understand the maintenance needed for it. 
