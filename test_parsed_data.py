import numpy as np
import matplotlib.pyplot as plt

fps = 30
angles = []
nframes = []

# Read the parsed data (I could parse it again, but it takes some time)
with open('prototype_raw_data.csv') as file:
    for line in file:
        nframe, angle = map(int, line.strip().split(','))
        angles.append(angle)
        nframes.append(nframe)

# Count full turns, add 360 degrees for each one
# Assumes 1) the values strictly increase 2) no full turn was skipped
# Otherwise we're in trouble.
turn = 0
for i in range(1, len(angles)):
    angles[i] += 360 * turn
    if angles[i] < angles[i - 1]:
        turn += 1
        angles[i] += 360

# Convert to physically true units
angles = list(map(lambda angle: (angle - angles[0]) / 180 * np.pi, angles))
times = list(map(lambda nframe: (nframe - nframes[0]) / fps, nframes))

# Plot and save the plot to a file soon to be deleted
plt.scatter(times, angles)
plt.savefig('figures/tmp_plot.png')
