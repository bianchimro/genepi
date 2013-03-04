Optimizing with the genetic algorithm
=====================================

In general, to use genepi as an optimization framework, you'll have to create an instance
of the GeneticAlgorithm class, with parameters suitable for your optimization needs, and
call its "evolve" method.

Such parameters consist of:

* A required protogenome instance
* A required fitness function
* An optional set of parameters describing the evolution strategy termination criteria


The protogenome
---------------

The protogenome represents the "model" of individuals.


The fitness function
--------------------

The fitness function expresses the goal we want to achieve during optimization.


Stop criteria
-------------
Once the genetic algorithm "evolve" method is called, evolution continues until some condition
is verified. 

This condition must be expressed with one or more "stop criteria", which are
functions that take the genetic algorithm as a parameter and returns True if the evolution
should stop and False otherwise.
Stop criteria can be fed with other parameters, that come directly from the GeneticAlgorithm
constructor.

After each generation has been evaluated, all the stop criteria are evaluated in sequence,
and if one of them returns True, evolution stops. If multiple stop criteria are set for
a genetic algorithm, evolution stops if just one of them evaluates to True.

Notice that you cannot call the 'evolve' method without defining at least one termination
criteria, or an exception will be raised.


Selection settings
------------------


Crossover settings
------------------


Mutation settings



