from functions import bukin_2d
from genetic_algorithm import GeneticAlgorithm

# Experiment 1
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

# ----------------------------------------------------------------

def test_for_param_grid(param_grid):
  # Create all combinations of parameters
  param_combinations = list(itertools.product(
      param_grid['population_size'],
      param_grid['mutation_rate'],
      param_grid['mutation_strength'],
      param_grid['crossover_rate'],
      param_grid['generations']
  ))
  results = []

  for combo in param_combinations:
      pop_size, mut_rate, mut_str, cross_rate, gens = combo

      ga = GeneticAlgorithm(
            population_size=pop_size,
            mutation_rate=mut_rate,
            mutation_strength=mut_str,
            crossover_rate=cross_rate,
            num_generations=gens,
            objective_function=bukin_2d,
            init_ranges=((-15, 5), (-3, 3)),
        )
      best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=42)
      score = best_fitness_values[-1]

      results.append({
          'Population Size': pop_size,
          'Mutation Rate': mut_rate,
          'Mutation Strength': mut_str,
          'Crossover Rate': cross_rate,
          'Generations': gens,
          'Score': score
      })

  df = pd.DataFrame(results)

  return df.sort_values(by='Score').head(10)

# Finding best parameters
param_grid = {
    'population_size': [20, 50, 100, 200],
    'mutation_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
    'mutation_strength': [0.1, 0.5, 1, 3],
    'crossover_rate': [0.2, 0.5, 0.8, 1],
    'generations': [ 20, 50, 100, 200]
}
test_for_param_grid(param_grid)

param_grid = {
    'population_size': [90, 100, 110, 120],
    'mutation_rate': [0.18, 0.2, 0.22, 0.25],
    'mutation_strength': [0.1, 0.5, 1, 3],
    'crossover_rate': [0.45, 0.5, 0.55, 0.6],
    'generations': [ 20, 50, 100, 200]
}
test_for_param_grid(param_grid)

# Verify best solution
ga = GeneticAlgorithm(
    population_size=120,
    mutation_rate=0.25,
    mutation_strength=1,
    crossover_rate=0.55,
    num_generations=200,
    objective_function=bukin_2d,
    init_ranges=((-15, 5), (-3, 3)),
)

best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=42)
print(f"Best solution: {best_solutions[-1]}")
print(f"Best fitness: {best_fitness_values[-1]}")
print(f"Average fitness: {average_fitness_values[-1]}")

# ----------------------------------------------------------------

# Testing different seed values
for seed in [18, 28, 45, 180, 2390]:
  ga = GeneticAlgorithm(
    population_size=120,
    mutation_rate=0.25,
    mutation_strength=1,
    crossover_rate=0.55,
    num_generations=200,
    objective_function=bukin_2d,
    init_ranges=((-15, 5), (-3, 3)),
   ) 

  best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=seed)
  print(f"For seed {seed}\t best solution: {np.round(best_solutions[-1], 3)}\t best fitness: {np.round(best_fitness_values[-1], 3)}\taverage fitness: {np.round(average_fitness_values[-1], 3)}")

def test_for_param_grid_with_seed(param_grid, seeds):
  # Create all combinations of parameters
  param_combinations = list(itertools.product(
      param_grid['population_size'],
      param_grid['mutation_rate'],
      param_grid['mutation_strength'],
      param_grid['crossover_rate'],
      param_grid['generations']
  ))
  results = []

  for combo in param_combinations:
      pop_size, mut_rate, mut_str, cross_rate, gens = combo

      ga = GeneticAlgorithm(
            population_size=pop_size,
            mutation_rate=mut_rate,
            mutation_strength=mut_str,
            crossover_rate=cross_rate,
            num_generations=gens,
            objective_function=bukin_2d,
            init_ranges=((-15, 5), (-3, 3)),
        )
      score = 0.0
      for seed in seeds:
        best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=42)
        score += best_fitness_values[-1]

      results.append({
          'Population Size': pop_size,
          'Mutation Rate': mut_rate,
          'Mutation Strength': mut_str,
          'Crossover Rate': cross_rate,
          'Generations': gens,
          'Score': score
      })

  df = pd.DataFrame(results)

  return df.sort_values(by='Score').head(10)

# time about 11m
param_grid = {
    'population_size': [90, 100, 110, 120],
    'mutation_rate': [0.18, 0.2, 0.22, 0.25],
    'mutation_strength': [0.1, 0.5, 1, 3],
    'crossover_rate': [0.45, 0.5, 0.55, 0.6],
    'generations': [ 20, 50, 100, 200]
}
seeds = [18, 28, 45, 180, 2390]
test_for_param_grid_with_seed(param_grid, seeds)


# ----------------------------------------------------------------

seeds = [18, 28, 45, 180, 2390]
populations = [120, 60, 30, 10]

for seed in seeds:
  for pop in populations:
      ga = GeneticAlgorithm(
        population_size=pop,
        mutation_rate=0.25,
        mutation_strength=1,
        crossover_rate=0.55,
        num_generations=200,
        objective_function=bukin_2d,
        init_ranges=((-15, 5), (-3, 3)),
      ) 

      best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=seed)
      print(f"{seed}\t {pop}\t {np.round(best_solutions[-1], 3)}\t {np.round(best_fitness_values[-1], 3)}\t {np.round(average_fitness_values[-1], 3)}")


# ----------------------------------------------------------------
# Testing by changing one parameter at a time
import matplotlib.pyplot as plt
import pandas as pd
import random

def test_for_fixed_params(fixed_params, param_to_vary, test_values):

  results = []

  for val in test_values:
      params = fixed_params.copy()
      params[param_to_vary] = val

      ga = GeneticAlgorithm(
            population_size=params['population_size'],
            mutation_rate=params['mutation_rate'],
            mutation_strength=params['mutation_strength'],
            crossover_rate=params['crossover_rate'],
            num_generations=params['generations'],
            objective_function=bukin_2d,
            init_ranges=((-15, 5), (-3, 3)),
        )
      best_solutions, best_fitness_values, average_fitness_values = ga.evolve(seed=42)
      score = best_fitness_values[-1]

      results.append({
          param_to_vary: val,
          'Score': score,
          'solution_x': best_solutions[-1].x,
          'solution_y': best_solutions[-1].y,
      })

  df = pd.DataFrame(results).sort_values(by='Score').head(40)

  plt.figure(figsize=(8, 5))
  plt.subplot(121)
  plt.scatter(df[param_to_vary], df['Score'], color='blue', s=20)
  plt.title(f"Effect of {param_to_vary.replace('_', ' ').title()} on Score")
  plt.xlabel(param_to_vary.replace('_', ' ').title())
  plt.ylabel("Score")
  plt.grid(True)
  plt.subplot(122)
  plt.scatter(df['solution_x'], df['solution_y'], color='red', s=20)
  plt.title(f"Solutions")
  plt.xlabel("x")
  plt.ylabel("y")
  plt.grid(True)
  plt.show()

    fixed_params = {
    'population_size': 120,
    'mutation_rate': 0.25,
    'mutation_strength': 1,
    'crossover_rate': 0.55,
    'generations': 100
}
param_to_vary = 'population_size'
test_values = [x for x in range(50, 150, 2)]

test_for_fixed_params(fixed_params, param_to_vary, test_values)

param_to_vary = 'mutation_rate'
test_values = [x for x in np.linspace(0.1, 0.3, 50)]

test_for_fixed_params(fixed_params, param_to_vary, test_values)

param_to_vary = 'mutation_strength'
test_values = [x for x in np.linspace(0, 0.5, 50)]

test_for_fixed_params(fixed_params, param_to_vary, test_values)

param_to_vary = 'crossover_rate'
test_values = [x for x in np.linspace(0.4, 0.6, 50)]

test_for_fixed_params(fixed_params, param_to_vary, test_values)

param_to_vary = 'generations'
test_values = [x for x in range(1, 200, 4)]

test_for_fixed_params(fixed_params, param_to_vary, test_values)

