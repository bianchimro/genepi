Introduction
============

**genepi** is a genetic algorithm-based optimization framework written in Python.


(Motivation of genepi, inspiration, and ideas behind it.)
...
...

The genepi package is written to be:

* Extensible at various levels (gene representation, crossover/mutation/selection methods
  and strategies, stop criteria, cache and storage backend, ...)
* Easily applicable to complex fitness functions
* Tested: genepi relies on nose and coverage for testing,
  with two testing suites, unit and integration tests.


Some features:

* Extensible cache backend
* Extensible storage backend  


Ideas in the pipeline:

* Resumable evolution (via storage backends): allow load evolution data from a storage 
  backend and restart from the last saved point.
* Distributed evolution: allow to use a distributed task queue for performing fitness
  evaluation.
* Command line utilities to perform evolution from declarative python files (fabric style)
* Interactive evolution: setting a "manual" stop criterium



  
  
  
  



  