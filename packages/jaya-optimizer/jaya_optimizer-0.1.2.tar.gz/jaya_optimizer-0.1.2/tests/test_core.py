import unittest
import numpy as np
from jaya_algorithm.core import JayaOptimizer

class TestJayaOptimizer(unittest.TestCase):
    def test_simple_minimization(self):
        """Test the algorithm on a simple minimization problem."""
        def objective_function(X):
            return np.sum(X**2)  # Minimize the sum of squares

        boundaries = [[-10, 10]] * 2  # Two variables with bounds [-10, 10]
        optimizer = JayaOptimizer(function=objective_function, dimension=2, variable_boundaries=boundaries, max_iterations=50, population_size=10)
        best_solution, best_value, history = optimizer.optimize()

        self.assertLessEqual(best_value, 1e-2, "Optimization did not converge to the minimum.")

    def test_boundary_conditions(self):
        """Ensure that solutions stay within the variable boundaries."""
        def objective_function(X):
            return np.sum(X)

        boundaries = [[0, 5]] * 3  # Three variables with bounds [0, 5]
        optimizer = JayaOptimizer(function=objective_function, dimension=3, variable_boundaries=boundaries, max_iterations=50, population_size=10)
        best_solution, best_value, history = optimizer.optimize()

        self.assertTrue(np.all(best_solution >= 0) and np.all(best_solution <= 5), "Solution is outside boundaries.")

    def test_invalid_boundaries(self):
        """Check if invalid boundaries raise an error."""
        def objective_function(X):
            return np.sum(X)

        with self.assertRaises(ValueError):
            boundaries = [[0, 5], [0]]  # Invalid boundary definition
            JayaOptimizer(function=objective_function, dimension=2, variable_boundaries=boundaries)

    def test_user_inputs(self):
        """Test if user inputs are prompted when parameters are missing."""
        def objective_function(X):
            return np.sum(X**2)

        # Mocking user input for iterations and population size
        with unittest.mock.patch('builtins.input', side_effect=["30", "15"]):
            boundaries = [[0, 1]] * 2
            optimizer = JayaOptimizer(function=objective_function, dimension=2, variable_boundaries=boundaries)
            self.assertEqual(optimizer.max_iterations, 30)
            self.assertEqual(optimizer.population_size, 15)

if __name__ == "__main__":
    unittest.main()
