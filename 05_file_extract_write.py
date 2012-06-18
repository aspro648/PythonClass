# Find power.csv file for a single simulation.
# Parse file for the final Total Power
# (last line, right-most column) and save
# value to outFile.csv


# open and read file

# parse file for info

# write out info to new file

import os, sys

DEBUG = True # simpler than using Python's logging module

base_dir = os.getcwd()
sim = 'sim_files'
target_dir = 'lr0'
target_file = 'power.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)
if DEBUG: print target_path

f = open(target_path, 'r')
lines = f.readlines()
f.close()

# strip whitespace
while lines[-1].strip() == '':
    lines = lines[:-1]

line = lines[-1]
if DEBUG: print line

if DEBUG: print line.split()

if DEBUG: print line.split(',')

if DEBUG: print line.split(',')[-1]

pTotal = line.split(',')[-1]
if DEBUG: print 'pTotal = %s' % pTotal

outFile = open(os.path.join(base_dir, 'outFile.txt'), 'w')
outFile.write('sim,pTotal\n')
outFile.write('%s,%s' % (target_dir, pTotal))
outFile.close()
