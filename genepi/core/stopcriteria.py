def convergence_stop(ga_engine, **options):
   pop = ga_engine.population
   return pop.individuals[0] == pop.individuals[-1]
   
def raw_score_stop(ga_engine, **options):
    stop_score = options.get('stop_score')
    return ga_engine.best_individual().score <= stop_score
