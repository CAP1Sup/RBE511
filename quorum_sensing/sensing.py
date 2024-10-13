import os
import random

import matplotlib.pyplot as plt
import numpy as np
from agent import Agent, State

# Sizes of the grids
WIDTHS = [5, 10, 20]
HEIGHTS = [5, 10, 20]

# Probability of a cell initiating a signal wave
P = 0.0001

# Refractory period of a cell
# This is the time it takes for a cell to recover from a signal wave
R = 10

# The number of neighbors to consider when infecting
# Should be 4 or 8
NEIGHBORHOOD = 8

# Number of simulations to run per size
SIMULATIONS = 25


# Grid printing function, used for debugging
def print_grid_agents(grid):
    counter = 0
    for row in grid:
        print(f"Row: {counter}")
        for index in row:
            print(index)
        print("\n")
        counter += 1


def print_grid_states(grid):
    print("Agent States:")
    for row in grid:
        for index in row:
            if index.state == State.REFRACTORY:
                print("R", end="")
            else:
                print("S", end="")
        print("")


def neighbors_of_4(agent: Agent, grid):
    neighbors = []
    row = agent.row
    col = agent.col
    if row > 0:
        neighbors.append(grid[row - 1][col])
    if row < H - 1:
        neighbors.append(grid[row + 1][col])
    if col > 0:
        neighbors.append(grid[row][col - 1])
    if col < W - 1:
        neighbors.append(grid[row][col + 1])
    return neighbors


def neighbors_of_8(agent: Agent, grid):
    neighbors = neighbors_of_4(agent, grid)
    row = agent.row
    col = agent.col
    if row > 0 and col > 0:
        neighbors.append(grid[row - 1][col - 1])
    if row > 0 and col < W - 1:
        neighbors.append(grid[row - 1][col + 1])
    if row < H - 1 and col > 0:
        neighbors.append(grid[row + 1][col - 1])
    if row < H - 1 and col < W - 1:
        neighbors.append(grid[row + 1][col + 1])
    return neighbors


def signal(agent: Agent):
    # Do nothing if the agent is already refractory
    if agent.state == State.REFRACTORY:
        return

    # Update this agent's state
    agent.state = State.REFRACTORY
    agent.refractory_steps_remaining = R
    agent.est_group_size += 1
    agent.steps_since_last_signal = 0


def is_before(neighbor: Agent, agent: Agent):
    return neighbor.row < agent.row or (
        neighbor.row == agent.row and neighbor.col < agent.col
    )


def has_signalled_neighbor(agent: Agent, grid):
    # Find the neighbors of this agent
    neighbors = []
    if NEIGHBORHOOD == 4:
        neighbors = neighbors_of_4(agent, grid)
    else:
        neighbors = neighbors_of_8(agent, grid)

    # Check if any of the neighbors have signalled
    for neighbor in neighbors:
        if not neighbor.state == State.REFRACTORY:
            continue

        # Check if the neighbor has been updated already
        if is_before(neighbor, agent):
            if neighbor.refractory_steps_remaining == R - 1:
                # They just signalled, so we should too
                return True
        # Is after
        elif neighbor.refractory_steps_remaining == R:
            return True

    # Default to False
    return False


def update(agent: Agent, grid):
    if agent.state == State.SUSCEPTIBLE:
        if has_signalled_neighbor(agent, grid):
            signal(agent)
        elif not agent.initiated_a_signal and random.random() < P:
            agent.initiated_a_signal = True
            signal(agent)
        else:
            agent.steps_since_last_signal += 1
    else:
        agent.steps_since_last_signal += 1
        if agent.refractory_steps_remaining > 0:
            agent.refractory_steps_remaining -= 1
            if agent.refractory_steps_remaining <= 0:
                agent.state = State.SUSCEPTIBLE


def is_done(agent: Agent):
    return agent.steps_since_last_signal >= 1 / P


average_estimates = []
for size in range(len(WIDTHS)):
    W = WIDTHS[size]
    H = HEIGHTS[size]
    average_estimate = 0

    for sim in range(SIMULATIONS):
        # Initialize the grid
        grid = []
        for row in range(H):
            grid.append([])
            for col in range(W):
                grid[row].append(Agent(row, col))

        # Progress tracking
        done = False
        iteration = 0

        # Main loop
        while not done:
            # Default to done, but set to False if any agent is not done
            done = True

            # Loop over all agents
            for row in range(H):
                for col in range(W):
                    # Update the agent's state
                    update(grid[row][col], grid)

                    # Check if the agent is done
                    if not is_done(grid[row][col]):
                        done = False

        # Calculate the average estimate
        total_estimate = 0
        for row in grid:
            for agent in row:
                total_estimate += agent.est_group_size
        average_estimate += total_estimate / (H * W) / SIMULATIONS

        # Print out that the simulation is done
        print(
            f"Simulation {sim} done for group size {H}x{W} with average estimate {average_estimate * SIMULATIONS/(sim+1):.2f}"
        )

    # Add the average estimate to the list
    average_estimates.append(average_estimate)

# Calculate the size titles
titles = []
for size in range(len(WIDTHS)):
    titles.append(f"{WIDTHS[size]}x{HEIGHTS[size]}")

# Calculate the sizes
counts = []
for size in range(len(WIDTHS)):
    counts.append(WIDTHS[size] * HEIGHTS[size])

# Scale the averages by their counts
average_proportions = [
    average_estimates[i] / counts[i] for i in range(len(average_estimates))
]

# Create a plot of the sizes
plt.figure(figsize=(8, 5))
plt.bar(titles, average_proportions)
plt.xlabel("Grid Size")
plt.ylabel("Average Estimated Group Size as Proportion of True Size")
plt.title(
    f"Avg Est Group Size Distribution With P={P}, R={R}, Distance={NEIGHBORHOOD} with {SIMULATIONS} Simulations"
)

# Create a custom x and y axis
# plt.xticks(np.arange(min(histogram.keys()), max(histogram.keys()) + 1, 1))
plt.yticks(
    np.arange(
        0,
        1 + 0.1,
        1 / 10,
    )
)

# Create a folder to store the plots (if it doesn't exist)
path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
if not os.path.exists(f"{path}/plots"):
    os.makedirs(f"{path}/plots")

# Save the plot to a file
plt.savefig(
    f"{path}/plots/plot_p_{P}_r_{R}_distance_{NEIGHBORHOOD}.jpeg", format="jpeg"
)

# plt.show()
