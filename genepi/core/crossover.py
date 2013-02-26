def genome_add(genome_a, genome_b):
    return genome_a + genome_b
    
def genome_choose(genome_a, genome_b):
    return random.choice([genome_a, genome_b])
    
def single_point_crossover(genome_a, genome_b):
    return genome_a.crossover(genome_b)
