def convergence_stop(ga_engine, **options):
    #pop = ga_engine.population
    #return pop.individuals[0].score == pop.individuals[-1].score
    num_generations = options.get('num_generations', 10)
    if ga_engine.generation < num_generations:
        return False
    stats = ga_engine.population_stats
    if ga_engine.optimization_mode == 'min':
        key = 'min_score'
    else:
        key = 'max_score'
    scores = [x[key] for x in stats[-num_generations:]]
    return len(set(scores)) == 1


   
   
def raw_score_stop(ga_engine, **options):
    stop_score = options.get('stop_score')
    if ga_engine.optimization_mode == 'min':
        return ga_engine.best_individual().score <= stop_score
    else:
        return ga_engine.best_individual().score >= stop_score