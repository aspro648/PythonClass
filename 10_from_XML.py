# Use built-in minidom module to extract 'topsideConvectiveHTCoeff',
# 'topsideAirVelocity', and 'topsideConvectiveMTCoeff1' from simulation_data.xml.


import matplotlib.pyplot as plt
import numpy as np
import os, sys
from xml.dom import minidom
# Only need 'minidom.~' instead of 'xml.dom.minidom.~'
# to call these methods.


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
    return pTotal


target_file = 'simulation_data.xml'
xmldoc = minidom.parse(os.path.join(base_dir, sim, 'lr0', target_file))
node = xmldoc.getElementsByTagName("topsideConvectiveHTCoeff")[0]
if DEBUG: print node.toxml()
unit = node.getAttribute('units').strip()
info = node.getAttribute('info').strip()
data = node.childNodes[0].data.strip()
if DEBUG: print info, data, unit


def getXML(target_dir, element_tags):
    '''Use minidom to extract values from simulation_data.xml.
       Returns a dictionary of (element_tag:value) pairs.'''
    return_dict = {}
    target_file = 'simulation_data.xml'
    xmldoc = minidom.parse(os.path.join(base_dir, sim, target_dir, target_file))

    for element_tag in element_tags:
        node = xmldoc.getElementsByTagName(element_tag)[0]
        if DEBUG: print node.toxml()
        unit = node.getAttribute('units').strip()
        info = node.getAttribute('info').strip()
        data = node.childNodes[0].data.strip()
        return_dict[element_tag] = data
        if DEBUG: print info, data, unit
    return return_dict


print getXML('lr0', ['topsideConvectiveHTCoeff'])

# build a list of directories to parse
dir_list = os.listdir(os.path.join(base_dir, sim))
if DEBUG: print 'dir_list = %s' % dir_list
out_text = ''

#xml values to extract from simulation_data.xml
element_tags = [ 'topsideConvectiveHTCoeff', 'topsideAirVelocity',
         'topsideConvectiveMTCoeff1' ]

# Extract required data from each directory
DEBUG = False
for sim_dir in dir_list:
    if sim_dir.find('lr') == 0: # found a sim run
        pTotal = getPtotal(sim_dir)
        topAirVelocity = getTopAirVelocity(sim_dir)
        topAirTemperature = getTopAirTemperature(sim_dir)
        xml_vals = getXML(sim_dir, element_tags)
        out_line = '%s/%s,%s,%s,%s' % (sim, sim_dir, pTotal, topAirVelocity,
                                       topAirTemperature)
        for element in element_tags:
            out_line = out_line + ',' + xml_vals[element]
        if DEBUG: print out_line + '\n',
        out_text += out_line + '\n'
        
# open file and write out header and data
outFile = open(os.path.join(base_dir, 'outFile.txt'), 'w')
outFile.write('sim,pTotal,topAirVeleocity, topAirTemperature')
for element in element_tags:
    outFile.write(',' + element)
outFile.write('\n')
outFile.write(out_text)
outFile.close()

# load data from file we created
pTotal, topAirVelocity, topAirTemperature = np.loadtxt('outFile.txt', delimiter=',',
                                                       skiprows=1, unpack=True,
                                                       usecols=(1,2,3))
# assign contour axises
x = topAirTemperature
y = topAirVelocity
z = pTotal

# Numpy tricks for contour plot
np.indices = np.lexsort(keys = (x, y))
x = np.unique(x)
y = np.unique(y)
X,Y = np.meshgrid(x, y)
v = 0
tempZ = []

for yy in range(len(y)):
    zz = []
    for xx in range(len(x)):
        zz.append(z[np.indices[v]])
        v += 1
    tempZ.append(zz)
Z = np.array(tempZ)
plt.clf()
plt.hold(True) #put contour over contourf
plt.contourf(X, Y, Z, 9)
CS = plt.contour(X,Y,Z, 9, colors='k')
plt.xlim(np.min(x),np.max(x))
plt.ylim(np.min(y),np.max(y))

title = 'Evaporative Power (W)'
plt.title(title, fontsize=14, color='b')

xlabel = 'Air Temperature (C)'
plt.xlabel(xlabel, fontsize=14)

ylabel = 'Air Velocity (m/s)'
plt.ylabel(ylabel, fontsize=14)

#contour labels
plt.clabel(CS, CS.levels, inline=True, fontsize=10, colors='k', fmt='%g')

plt.savefig('EvaporativePower.png')



