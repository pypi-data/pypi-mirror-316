import numpy as np

class JayaOptimizer:
    def __init__(self, function, dimension, variable_boundaries, max_iterations=None, population_size=None):
        """
        Initialize the Jaya Optimization Algorithm.

        Parameters:
        - function: Objective function to minimize or maximize.
        - dimension: Number of decision variables.
        - variable_boundaries: Array of [min, max] for each variable.
        - max_iterations: Maximum number of iterations (optional; will prompt user if not provided).
        - population_size: Number of individuals in the population (optional; will prompt user if not provided).
        """
        self.function = function
        self.dimension = dimension
        self.variable_boundaries = np.array(variable_boundaries)

        if max_iterations is None:
            self.max_iterations = int(input("Enter the maximum number of iterations: "))
        else:
            self.max_iterations = max_iterations

        if population_size is None:
            self.population_size = int(input("Enter the population size: "))
        else:
            self.population_size = population_size

        # Ensure variable boundaries are valid
        if self.variable_boundaries.shape != (dimension, 2):
            raise ValueError("Variable boundaries must be a (dimension x 2) array.")

    def initialize_population(self):
        """
        Initialize the population within the variable boundaries.
        """
        return np.random.uniform(
            low=self.variable_boundaries[:, 0],
            high=self.variable_boundaries[:, 1],
            size=(self.population_size, self.dimension)
        )

    def optimize(self):
        """
        Execute the Jaya Optimization Algorithm.
        Returns:
        - Best solution found.
        - Objective function value at the best solution.
        """
        population = self.initialize_population()

        for iteration in range(self.max_iterations):
            # Evaluate objective function for all individuals
            fitness = np.apply_along_axis(self.function, 1, population)

            # Find the best and worst solutions in the population
            best_index = np.argmin(fitness)
            worst_index = np.argmax(fitness)

            best_solution = population[best_index]
            worst_solution = population[worst_index]

            # Update each individual's position
            for i in range(self.population_size):
                r1 = np.random.uniform(size=self.dimension)
                r2 = np.random.uniform(size=self.dimension)

                # Calculate new position based on Jaya algorithm formula
                new_position = population[i] + r1 * (best_solution - abs(population[i])) - r2 * (worst_solution - abs(population[i]))

                # Ensure new position is within bounds
                new_position = np.clip(new_position, self.variable_boundaries[:, 0], self.variable_boundaries[:, 1])

                # Replace the individual's position
                population[i] = new_position

        # Final best solution after all iterations
        final_fitness = np.apply_along_axis(self.function, 1, population)
        best_index = np.argmin(final_fitness)
        return population[best_index], self.function(population[best_index])
