def run_simulation(genomes, config):

    import neat

    # Initialise NEAT
    nets = []
    cars = []

    for id in genomes:
        net = neat.nn.FeedForwardNetwork.create(id, config)
        nets.append(net)
        id.fitness = 0