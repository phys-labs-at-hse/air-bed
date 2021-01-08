import math
import matplotlib.pyplot as plt

# Read the data
data_file_path_in  = 'csv_data/9.csv'
data_file_path_out = 'csv_data/9_fixed.csv'
angles, times = [], []
with open(data_file_path) as file:
    for line in file:
        time, angle = map(float, line.strip().split(','))
        times.append(time)
        angles.append(angle)
plt.scatter(times, angles)

jump_time = 17
times_before = list(filter(lambda time: time < jump_time, times))
angles_before = angles[:len(times_before)]
times_after = times[len(times_before):]
angles_after = angles[len(times_before):]

plt.scatter(times_before, angles_before)
plt.scatter(times_after, angles_after)

angles_after = list(map(lambda angle: angle - 2 * math.pi, angles_after))

plt.scatter(times_before, angles_before)
plt.scatter(times_after, angles_after)

# Write the data back. I replace the file manually to avoid mistakes
angles = angles_before + angles_after
with open(data_file_path_out, 'a') as file:
    for angle, time in zip(angles, times):
        file.write(f'{time},{angle}\n')
