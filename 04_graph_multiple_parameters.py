# Open 'power.csv' file and load data.
# Create a graph of Sensible, Latent, and Total Power


import matplotlib.pyplot as plt
import numpy as np
import os, sys

DEBUG = True

base_dir = os.getcwd()
sim = 'sim_files'
target_dir = 'lr0'
target_file = 'vapor.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)
if DEBUG: print target_path

distance, time, temperature, percentRemaining, \
    dryingRate = np.loadtxt(target_path, \
    delimiter = ',', skiprows=3, unpack=True, \
    usecols=(range(0,5)))

target_file = 'power.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)

Pevap, Pweb, Pink, Ptotal, = np.loadtxt(target_path, \
    delimiter = ",", skiprows=3, unpack=True,
    usecols=(1,2,3,4))

plt.plot(distance, Ptotal, label='Total')
plt.plot(distance, Pevap, label='Latent')
plt.plot(distance, Pweb, label='Sensible')

plt.grid(True)
plt.legend(loc='best')

title = 'Cumulative Power'
plt.title(title, fontsize='x-large', color='b', weight='bold')

xlabel = 'Distance (cm)'
plt.xlabel(xlabel)

ylabel = 'Power (W)'
plt.ylabel(ylabel, fontsize='large')

plt.savefig('CumulativePower.png')
plt.show()


    
