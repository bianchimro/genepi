Overview
========




Optimization and fitness
------------------------

First of all, genepi is an **optimization** framework.

as wikipedia states at the page http://en.wikipedia.org/wiki/Mathematical_optimization: ::


   ...
   in the simplest case, an optimization problem consists of maximizing or minimizing a
   real function by systematically choosing input values from within an allowed set and
   computing the value of the function.
   ...
   ...
   The function f is called, variously, an objective function, cost function (minimization),
   indirect utility function (minimization), utility function (maximization), or, in
   certain fields, energy function, or energy functional.
   ...


When performing an optimization, we might be interested in:

* Finding the optimal value
* Finding the optimal input arguments


Genetic algorithms model the search for optimal input arguments after biological evolution.
In this model:
    
* The function that we want to minimize or maximized is called the **fitness function**.
* Each set of input arguments (solutions) of by the fitness function is referred to as an
  "Individual".


Again, here is what Wikipedia says: ::

   A fitness function is a particular type of objective function that is used to summarise, 
   as a single figure of merit, how close a given design solution is to achieving the set aims.


In this context, optimize means finding the best individual, the one that performs 
better according to the fitness function.
    


The genetic algorithm
---------------------

GeneticAlgorithm:  simulates the evolution of a Population in order to create individuals
that "behave well" with respect to a given "fitness function"

   
* create an initial population
* evaluate each individual in the population using the fitness function
* while the best individual in population does not satisfy some criteria:
   * choose some individuals from the population
   * create some new individuals starting from them
   * optionally slightly change these new individuals
   * replace the population with new created individuals 
   * evaluate each individual in the population using the fitness function
      
   
--------------------------------------------






Population: is a collection of individuals. Each individual is an instance of a Genome

Genome: is a collection of Genes.

Gene: a small piece of information characterizing the genome. In the context of optimization of
a fitness function, this is practically limited by the sensitivity of the fitness function with respect to this gene.

ProtoGenome:

ProtoGene: 