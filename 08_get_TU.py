# Create a function to open 'vapor.out'
# and return value for 'TU' (topside air temperature).


import os, sys

DEBUG = True

base_dir = os.getcwd()
sim = 'sim_files'
target_dir = 'lr0'
target_file = 'power.csv'
target_path = os.path.join(base_dir, sim, target_dir, target_file)
if DEBUG: print 'target_path = %s' % target_path


def getTopAirTemperature(target_dir):
    ''' Return topAirTemperature ("TU") from 'vapor.out'. '''
    topAirTemperature = ''
    target_file = 'vapor.out'
    f = open(os.path.join(base_dir, sim, target_dir, target_file), 'r')
    lines = f.readlines()
    f.close()
    #line = '         TU = 0.2000E+02 deg C       HU  = 0.2337E+02 Cal/sqm/sec/deg C'
    for line in lines:
        if 'TU =' in line:
            topAirTemperature = line.split()[2]
            break
    return topAirTemperature


def getTopAirVelocity(target_dir):
    ''' Return topAirVelocity from variablesDME.txt
        Example of line-by-line parse of text file.'''
    topAirVelocity = ''
    target_file = 'variablesDME.txt'
    f = open(os.path.join(base_dir, sim, target_dir, target_file), 'r')
    lines = f.readlines()
    f.close()    
    for line in lines:
        line = line.split('#')[0] # remove comments
        if line.find('TopAirVelocity1') == 0:
            topAirVelocity = line.split()[-1]
            break
    return topAirVelocity


def getPtotal(target_dir):
    ''' Return pTotal from final entry in power.csv.
        Example of when we know where data will be. '''
    target_file = 'power.csv'    
    f = open(os.path.join(base_dir, sim, target_dir, target_file), 'r')
    lines = f.readlines()
    f.close()

    # strip whitespace
    while lines[-1].strip() == '':
        lines = lines[:-1]

    line = lines[-1]
    pTotal = line.split(',')[-1].strip()
    #if DEBUG: print '%s/%s : pTotal = %s' % (sim, target_dir, pTotal)
    return pTotal


#print getTopAirTemperature('lr0')
#exit()

# build a list of directories to parse
dir_list = os.listdir(os.path.join(base_dir, sim))
if DEBUG: print 'dir_list = %s' % dir_list
out_text = ''

# Extract required data from each directory
for sim_dir in dir_list:
    if sim_dir.find('lr') == 0: # found a sim run
        pTotal = getPtotal(sim_dir)
        topAirVelocity = getTopAirVelocity(sim_dir)
        topAirTemperature = getTopAirTemperature(sim_dir)
        out_line = '%s/%s,%s,%s,%s\n' % (sim, sim_dir, pTotal,
                                         topAirVelocity, topAirTemperature)
        if DEBUG: print out_line,
        out_text += out_line
        
# open file and write out header and data
outFile = open(os.path.join(base_dir, 'outFile.txt'), 'w')
outFile.write('sim,pTotal,topAirVeleocity, topAirTemperature\n')
outFile.write(out_text)
outFile.close()
