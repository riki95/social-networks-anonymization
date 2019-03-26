# Social Networks Anonymization

This project is part of the Data Protection & Privacy exam for the MSc in Computer Science at University of Genoa.
It consists in implementing the algorithm and methods used inside the paper, that can be found into the repo, and comparing the results found with the ones reported into the paper.

We use the NetworkX library in Python to work with graph and we implement Vertex Refinement Queries, Subgraph knowledge queries on two main datasets: Enron and Hep-th.

Then we perturbate the graph to achieve anonymity.

## Dataset

The datasets used are:

* Enron: https://www.cs.cmu.edu/~./enron/
* Hep-th: https://snap.stanford.edu/data/cit-HepTh.html

Both dataset have been parsed and compressed and the code to obtain the final data can be found inside the repo.

## Code

The code can be tested using

```
python main.py
```

The main file calls the methods inside other files.

## Authors

* Riccardo Basso
* Davide Ponzini
* Daniele Traversaro
