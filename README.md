# Master Plan

This tool gives students in graduate programs with different tracks the ability to verify their existing plan meets any specific requirements for classes.

## Limitations

Presently, there is only one plan definition for Portland State University. The format of the file should be extensible enough to support similar plans at other schools.

## Example Usage

An example `plan.json` is provided to show how to describe a plan. It is simply a list of desired classes.

The default behavior is to simply process your plan and show what tracks you meet as well as the number of credits.

```
$ ./cs.py --school pdx.json plan.json
***** Plan meets requirements for tracks: core, lang, sys
Credits 45/45
```

To view the plan in a human-readable format, simply add `--showplan`.

```
$ ./cs.py --showplan --school pdx.json plan.json
***** Plan meets requirements for tracks: core, lang, sys
Credits 45/45
--------- Plan ----------
CS 558: Programming Languages (Fall 2012)
CS 533: Concepts of Operating Systems (Winter 2013)
CS 581: Theory of Computation (Spring 2013)
CS 547: Computer Graphics (Fall 2013)
CS 553: Design Patterns (Winter 2014)
CS 510: Adv. Programming Language Implementation (Spring 2014)
CS 591: Intro. to Computer Security (Fall 2014)
CS 510: Intro. to Visual Computing (Winter 2015)
CS 510: Languages & Low-Level Programming (Spring 2015)
CS 510: Accelerated Computing with GPUs, APUs, and FPGAs (Summer 2015)
CS 594: Internetworking Protocols (Fall 2015)
CS 510: Network Security (Winter 2016)
CS 572: Operating Systems Internals (<Term> <XXXX>)
CS 592: Malware (<Term> <XXXX>)
CS 584: Algorithm Design and Analysis (<Term> <XXXX>)

```

For a more detailed analyis, add `-v`.

```
./cs.py -v  plan.json              
*********** Track: core **************
Have required CS 581: Theory of Computation
Have required CS 558: Programming Languages
Have required CS 533: Concepts of Operating Systems
Plan meets requirements for core
*********** Track: db **************
Missing required CS 586: Intro. to Database Management Systems
Missing required CS 587: Relational Database Management Systems
Missing too many optionals!
0/1 optionals
Plan does not meet requirements for db
*********** Track: ai **************
Missing required CS 541: Artificial Intelligence
Missing required CS 545: Machine Learning
Missing too many optionals!
0/1 optionals
Plan does not meet requirements for ai
*********** Track: lang **************
Have required CS 558: Programming Languages
Have optional CS 553: Design Patterns
Have optional CS 510: Adv. Programming Language Implementation
Have optional CS 510: Languages & Low-Level Programming
Plan has required number of optionals
3/2 optionals
Plan meets requirements for lang
*********** Track: sec **************
Have required CS 591: Intro. to Computer Security
Missing required CS 585: Cryptography
Have optional CS 592: Malware
Plan has required number of optionals
1/1 optionals
Plan does not meet requirements for sec
*********** Track: eng **************
Missing required CS 554: Software Engineering
Have optional CS 553: Design Patterns
Missing too many optionals!
1/2 optionals
Plan does not meet requirements for eng
*********** Track: sys **************
Have required CS 533: Concepts of Operating Systems
Have required CS 594: Internetworking Protocols
Have optional CS 572: Operating Systems Internals
Plan has required number of optionals
1/1 optionals
Plan meets requirements for sys
*********** Track: theory **************
Have required CS 581: Theory of Computation
Have required CS 584: Algorithm Design and Analysis
Missing too many optionals!
0/1 optionals
Plan does not meet requirements for theory
***** Plan meets requirements for tracks: core, lang, sys
Credits 45/45
```
