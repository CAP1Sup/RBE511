from enum import IntEnum

import numpy as np

np.set_printoptions(precision=5, suppress=True)


class InertiaStrategy(IntEnum):
    CONSTANT = 0
    DECAYING = 1
    RANDOM = 2


# Define the Rastrigin function
def rastrigin(X):
    n = len(X)
    A = 10
    return A * n + sum([(x**2 - A * np.cos(2 * np.pi * x)) for x in X])


# Convenience function for printing
def print_result(trial: int, pos: np.ndarray, best_value: float):
    print(f"Trial {trial}:\nPosition:")
    for val in pos:
        if val >= 0 and np.any(pos < 0):
            print(f" {val:.5f}")
        else:
            print(f"{val:.5f}")
    print(f"Minimum Value:\n{best_value:.5f}\n")


# Particle class
class Particle:
    def __init__(self, dimensions, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.velocity = np.random.uniform(-1, 1, dimensions)
        self.best_position = self.position.copy()
        self.best_value = rastrigin(self.position)

    def update_velocity(self, global_best_position, w=0.5, c1=1.5, c2=1.5):
        r1, r2 = np.random.rand(), np.random.rand()
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive + social

    def update_position(self, bounds):
        self.position += self.velocity
        self.position = np.clip(self.position, bounds[0], bounds[1])
        current_value = rastrigin(self.position)
        if current_value < self.best_value:
            self.best_position = self.position.copy()
            self.best_value = current_value


# PSO algorithm
def pso(
    num_particles,
    dimensions,
    bounds,
    max_iter,
    inertia_strategy=InertiaStrategy.CONSTANT,
):
    swarm = [Particle(dimensions, bounds) for _ in range(num_particles)]
    global_best_position = min(swarm, key=lambda p: p.best_value).best_position

    # Set the inertia weight once
    if inertia_strategy == InertiaStrategy.RANDOM:
        w = np.random.uniform(0, 1)

    for t in range(max_iter):
        if inertia_strategy == InertiaStrategy.CONSTANT:
            w = 1
        elif inertia_strategy == InertiaStrategy.DECAYING:
            w = 1 - t / max_iter
        elif inertia_strategy == InertiaStrategy.RANDOM:
            pass  # w is already set
        else:
            raise ValueError(
                "Invalid inertia strategy. Choose from InertiaStrategy.CONSTANT, InertiaStrategy.DECAYING, or InertiaStrategy.RANDOM."
            )

        for particle in swarm:
            particle.update_velocity(global_best_position, w=w)
            particle.update_position(bounds)

        global_best_position = min(swarm, key=lambda p: p.best_value).best_position

    return global_best_position, rastrigin(global_best_position)


# Parameters
num_particles = 100
dimensions = 5
bounds = [-5.12, 5.12]
max_iter = 1000
trials = 10
inertia_strategy = InertiaStrategy.CONSTANT
print_values_in_table_format = False

# Run PSO for a given number of trials
best_positions = []
best_values = []

print(f"Running PSO with inertia strategy: {inertia_strategy.name}")

for trial in range(trials):
    best_position, best_value = pso(
        num_particles, dimensions, bounds, max_iter, inertia_strategy
    )
    best_positions.append(best_position)
    best_values.append(best_value)
    print(
        f"Trial {trial + 1}: Best position: {best_position}, Best value: {best_value}"
    )

if print_values_in_table_format:
    print("Solutions for table:")
    for i, pos in enumerate(best_positions):
        print_result(i + 1, pos, best_values[i])

    # Print the average and best results
    print_result("Average", np.mean(best_positions, axis=0), np.mean(best_values))
    overall_best_value = min(best_values)
    overall_best_position = best_positions[best_values.index(overall_best_value)]
    print_result("Best", overall_best_position, overall_best_value)
