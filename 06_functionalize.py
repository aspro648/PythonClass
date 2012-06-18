# Functionalize the routine to extract Total Power
# and use it to parse through all simulations,
# writing results to outFile.csv


# create list of simulations to parse

# call function to get value for each simulation

# write value to outFile


import os, sys

DEBUG = True

base_dir = os.getcwd()
sim = 'sim_files'
target_dir = 'lr0'
target_file = 'power.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)
if DEBUG: print 'target_path = %s' % target_path


def getPtotal(target_dir):
    ''' Return pTotal from final entry in power.csv '''
    target_file = 'power.csv'    
    f = open(os.path.join(base_dir, sim, target_dir, target_file), 'r')
    lines = f.readlines()
    f.close()

    # strip whitespace
    while lines[-1].strip() == '':
        lines = lines[:-1]

    line = lines[-1]
    pTotal = line.split(',')[-1].strip()
    if DEBUG: print '%s/%s : pTotal = %s' % (sim, target_dir, pTotal)
    return pTotal


out_text = ''
pTotal = getPtotal(target_dir)
out_text += '%s/%s,%s\n' % (sim, target_dir, pTotal)

'''
# build a list of directories to parse
dir_list = os.listdir(os.path.join(base_dir, sim))
if DEBUG: print 'dir_list = %s' % dir_list
out_text = ''

# Extract required data from each directory
for sim_dir in dir_list:
    if sim_dir.find('lr') == 0: # found a sim run
        pTotal = getPtotal(sim_dir)
        out_text += '%s/%s,%s\n' % (sim, sim_dir, pTotal)
'''

# open file and write out header and data
outFile = open(os.path.join(base_dir, 'outFile.txt'), 'w')
outFile.write('sim,pTotal\n')
outFile.write(out_text)
outFile.close()
