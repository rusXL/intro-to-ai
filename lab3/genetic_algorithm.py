import random
import numpy as np
from typing import NamedTuple


class Individual(NamedTuple):
    x: int
    y: int


def set_seed(seed: int) -> None:
    # set fixed random seed to make the results reproducible
    random.seed(seed)
    np.random.seed(seed)


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        mutation_rate: float,
        mutation_strength: float,
        crossover_rate: float,
        num_generations: int,
        objective_function: callable,
        init_ranges: tuple,
    ):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.crossover_rate = crossover_rate
        self.num_generations = num_generations
        self.objective_function = objective_function
        self.init_ranges = init_ranges  # ((x_min, x_max), (y_min, y_max))

    def initialize_population(self) -> list[Individual]:
        x_range, y_range = self.init_ranges
        return [
            Individual(random.uniform(*x_range), random.uniform(*y_range))
            for _ in range(self.population_size)
        ]

    def evaluate_population(self, population: list[Individual]) -> list[float]:
        return [self.objective_function(ind.x, ind.y) for ind in population]

    def selection(
        self,
        population: list[Individual],
        fitness_values: list[float],
        tournament_size: int = 3,
    ) -> list[Individual]:
        selected = []
        for _ in range(len(population)):
            competitors_idx = random.sample(range(len(population)), tournament_size)
            best_idx = min(competitors_idx, key=lambda i: fitness_values[i])
            selected.append(population[best_idx])
        return selected

    def crossover(self, parents: list[Individual]) -> list[Individual]:
        offspring = []
        num_to_crossover = int(self.crossover_rate * len(parents))
        for _ in range(num_to_crossover // 2):
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            alpha = random.random()
            child1 = Individual(
                alpha * p1.x + (1 - alpha) * p2.x,
                alpha * p1.y + (1 - alpha) * p2.y,
            )
            alpha = random.random()
            child2 = Individual(
                alpha * p2.x + (1 - alpha) * p1.x,
                alpha * p2.y + (1 - alpha) * p1.y,
            )
            offspring.extend([child1, child2])
        # fill remaining with random parents to preserve population size
        while len(offspring) < len(parents):
            offspring.append(random.choice(parents))
        return offspring

    def mutate(self, individuals: list[Individual]) -> list[Individual]:
        mutated = []
        num_to_mutate = int(self.mutation_rate * len(individuals))
        indices_to_mutate = random.sample(range(len(individuals)), num_to_mutate)

        for i, ind in enumerate(individuals):
            if i in indices_to_mutate:
                mutated_ind = Individual(
                    ind.x + np.random.normal(0, self.mutation_strength),
                    ind.y + np.random.normal(0, self.mutation_strength),
                )
                # clip values to stay within bounds
                mutated_ind = Individual(
                    np.clip(mutated_ind.x, *self.init_ranges[0]),
                    np.clip(mutated_ind.y, *self.init_ranges[1]),
                )
                mutated.append(mutated_ind)
            else:
                mutated.append(ind)
        return mutated

    def evolve(self, seed: int):
        set_seed(seed)
        population = self.initialize_population()

        best_solutions = []
        best_fitness_values = []
        average_fitness_values = []

        for generation in range(self.num_generations):
            fitness_values = self.evaluate_population(population)

            # track best solution
            best_idx = np.argmin(fitness_values)
            best_solutions.append(population[best_idx])
            best_fitness_values.append(fitness_values[best_idx])
            average_fitness_values.append(np.mean(fitness_values))

            # evolve
            parents = self.selection(population, fitness_values)
            offspring = self.crossover(parents)
            mutated_offspring = self.mutate(offspring)

            # update population
            population = mutated_offspring

        return best_solutions, best_fitness_values, average_fitness_values
