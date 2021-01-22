import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
from labtables import Table


times, angles = Table.read_csv('csv_data/friction_check.csv')
times = np.array(times)
angles = np.array(angles)

# Drop the last three values, they are trash.
times = times[:-3]
angles = angles[:-3]

# Plot the angular velocity. It is not linear.
plt.scatter(times, np.gradient(angles, times))
plt.xlabel('Время, с', fontsize=14)
plt.ylabel('Угловая скорость, рад/с', fontsize=14)
plt.grid()
plt.savefig('figures/tmp_plot_1.png', bbox_inches='tight')
plt.close()

# Fit angles as a function of times with an exponent.
def exponent(times_, angle_inf, k):
    return angle_inf * (1 - np.exp(- k * times_))

popt, pcov = scipy.optimize.curve_fit(exponent, times, angles)
print('model: (angle_inf, k) -> angle_inf * (1 - exp(- k * times))')
print(f'parameters: {popt}')
print(f'std: {np.sqrt(np.diag(pcov))}')

plt.plot(times, exponent(times, *popt), 'r-', label="Fitted curve")
plt.scatter(times, angles, label="Original curve")
plt.grid()
plt.savefig('figures/tmp_plot_2.png', bbox_inches='tight')
