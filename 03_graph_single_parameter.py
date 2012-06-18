# Open 'vapor.csv' file and load all data.
# Use matplotlib module to create a graph of
# Drying Rate (g/m^2/min) vs. Distance(cm)


import matplotlib.pyplot as plt
import numpy as np
import os, sys

DEBUG = True # simpler than using Python's logging module

base_dir = os.getcwd()
sim = 'sim_files'
target_dir = 'lr0'
target_file = 'vapor.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)
if DEBUG: print target_path

distance, time, temperature, percentRemaining, \
    dryingRate = np.loadtxt(target_path, \
    delimiter = ',', skiprows=4, unpack=True, \
    usecols=(range(0,5)))

plt.plot(distance, dryingRate)

plt.grid(True)

title = 'Drying Rate vs. Distance'
plt.title(title, fontsize='x-large', color='b', weight='bold')

xlabel = 'Distance (cm)'
plt.xlabel(xlabel)

ylabel = 'Drying Rate (g/m^2/min)'
#ylabel = r' Drying Rate $\mathsf{(g/m^2/min)}$'
plt.ylabel(ylabel, fontsize='large')

plt.savefig('DryingRateVsDistance.png')

plt.show()


    




