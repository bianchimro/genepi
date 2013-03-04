======
genepi
======
.. image:: https://travis-ci.org/bianchimro/genepi.png?branch=master

**genepi** is a genetic algorithm framework written in python.




Documentation
-------------

Documentation is being built with Sphinx and will come soon. You can build a partial
documentation by installing sphinx and issuing

.. code-block:: bash
   make html
   
in the docs folder of genepi source.

Until then, here is a little example.

.. code-block:: python

    from genepi.core.ga import GeneticAlgorithm
    from genepi.core.factories import protogene_factory
    from genepi.core.protogenome import ProtoGenome
    from genepi.core.gene import IntGene
    from genepi.core.stopcriteria import raw_score_stop
    from genepi.core.crossover import single_point_crossover
    from genepi.core.selectors import select_from_top
    
    
    #example fitness function
    #fitness is the sum of parameters
    def fitness_function(genome):
        score = 0.0
        for value in genome.list_value():
            score += value
        return score
    
    
    # example genetic algorithm
    # we want to minimize the sum of a list of 50 integer numbers from 0 to 10   
        
    protogenes = protogene_factory(IntGene, 'x', 50, min_value=0, max_value=10)
    protogenome = ProtoGenome(protogenes, mutation_probability = 0.1) 
        
    algo = GeneticAlgorithm(protogenome, fitness_function, 
        population_size = 200,
        optimization_mode = 'min',
        num_parents = 4,
        crossover_method = single_point_crossover,
        selection_method = select_from_top,
        termination_criteria=[raw_score_stop], stop_score=0)
        
    #main evolution cycle
    algo.evolve(debug=True)
    
    bi = algo.best_individual()
    print bi.score
    print bi.dict_value()
        
        
    
More examples can be found in test/integration_test folder.
