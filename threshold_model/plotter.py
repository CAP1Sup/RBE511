import os

import matplotlib.pyplot as plt
import numpy as np

# Constants
RUN_TITLE = " - Fixed Initial Thresholds"
FIG_SIZE = (20, 10)  # (width, height)
ROBOTS = 20
THRESHOLDS = 2
TIME_INDEX = 0
TASK_INDEX = 2
THRESHOLD0_INDEX = 3
THRESHOLD1_INDEX = 4

# Calculate the file path
filepath = os.path.join(os.path.dirname(__file__), "fixed_initial_threshold_data.dat")

# Open the file
data = []
with open(filepath, "r") as file:
    # Extract the data
    for line in file:
        data.append(line.split())

# Convert the data to a numpy array
data = np.array(data, dtype=float)

# Sort the data
robots = np.empty(ROBOTS, dtype=object)
for i in range(ROBOTS):
    if i == 0:
        robots[i] = data[::ROBOTS].transpose()
    else:
        robots[i] = data[i::ROBOTS].transpose()

# Replace the task number with the rolling average of the last 100 task numbers
for i in range(ROBOTS):
    for j in range(1, len(robots[i][TASK_INDEX])):
        robots[i][TASK_INDEX][j] = (
            robots[i][TASK_INDEX][j - 1] * 0.99 + robots[i][TASK_INDEX][j] * 0.01
        )

# Calculate the maximum time step
max_time_step = len(robots[0][TIME_INDEX])

# Plot time step vs task number
plt.figure(figsize=FIG_SIZE)
for i in range(ROBOTS):
    plt.plot(robots[i][TIME_INDEX], robots[i][TASK_INDEX], label=f"Robot {i}")
plt.title(f"Time Step vs Avg Task Number From Last 100 Steps{RUN_TITLE}")
plt.xlabel("Time Step")
plt.ylabel("Avg Task Number")
plt.xticks(np.arange(0, max_time_step + 1, 100))
plt.xlim(0, max_time_step)
max_task_index = int(np.max([robot[TASK_INDEX] for robot in robots]))
plt.yticks(np.arange(0, max_task_index + 1.5, 0.5))
plt.ylim(0, max_task_index + 1)
plt.legend()
plt.show()

# Plot time steps vs thresholds
for i in range(THRESHOLDS):
    plt.figure(figsize=FIG_SIZE)
    for j in range(ROBOTS):
        plt.plot(
            robots[j][TIME_INDEX], robots[j][THRESHOLD0_INDEX + i], label=f"Robot {j}"
        )
    plt.title(f"Time Step vs Threshold {i}{RUN_TITLE}")
    plt.xlabel("Time Step")
    plt.ylabel(f"Threshold {i}")
    plt.xticks(np.arange(0, max_time_step + 1, 100))
    plt.xlim(0, max_time_step)
    plt.ylim(0, 1000 + 1)
    plt.legend()
    plt.show()
