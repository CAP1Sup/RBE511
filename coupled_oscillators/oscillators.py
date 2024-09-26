import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# The k constant is the coupling constant with other oscillators
k = 0.5

# T is the threshold of the counter that will reset the oscillator
T = 100

# Set the size of the grid
grid_x_size = 10
grid_y_size = 10

# Set the number of iterations
iterations = 1000

# Initialize the grid values
c_values = np.random.randint(low=0, high=T, size=(grid_x_size, grid_y_size))
states = np.zeros((grid_x_size, grid_y_size), dtype=bool)

# Flashed oscillator counts for each iteration
flashed_oscillators = np.zeros(iterations, dtype=int)


# Define helper functions
def neighbor_flashed(x, y):
    # Check left
    if x != 0 and states[x - 1, y]:
        return True

    # Check right
    if x != grid_x_size - 1 and states[x + 1, y]:
        return True

    # Check up
    if y != 0 and states[x, y - 1]:
        return True

    # Check down
    if y != grid_y_size - 1 and states[x, y + 1]:
        return True

    # No neighbors flashed
    return False


# Run the simulation
for iteration in range(iterations):
    # Loop through all the oscillators
    for x in range(grid_x_size):
        for y in range(grid_y_size):
            # Get the value of the current oscillator
            c = c_values[x, y] + 1

            if neighbor_flashed(x, y):
                c = c + k * c

            # Check if the oscillator has reached the threshold
            if c >= T:
                states[x, y] = 1
                c = 0
            else:
                states[x, y] = 0

            # Update the oscillator value
            c_values[x, y] = c

    # Count the number of flashing oscillators
    flashed_oscillators[iteration] = np.sum(states)

# Create a new figure and set the titles
fig = plt.figure(figsize=(15, 5))
plt.title(f"Flashing Oscillators Over Time with k = {k}")
plt.xlabel("Iteration")
plt.ylabel("Number of Flashing Oscillators")

# Plot the number of flashing oscillators over time
plt.plot(range(iterations), flashed_oscillators)

# Save the figure to a PDF file
with PdfPages("./ex1.pdf") as pdf:
    fig.savefig(pdf, format="pdf")

# Display the plot
plt.show()
