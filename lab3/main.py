from functions import bukin_2d
from genetic_algorithm import GeneticAlgorithm

if __name__ == "__main__":
    # TODO Experiment 1...
    ga = GeneticAlgorithm(
        population_size=50,
        mutation_rate=0.1,
        mutation_strength=0.5,
        crossover_rate=0.7,
        num_generations=100,
        objective_function=bukin_2d,
        init_ranges=((-15, -5), (-3, 3)),
    )
    best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=18)

    print(f"Best solution: {best_solutions[-1]}")
    print(f"Best fitness: {best_fitness_values[-1]}")
    print(f"Average fitness: {average_fitness_values[-1]}")
