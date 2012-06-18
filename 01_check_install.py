# Script to check installation.
# These will all be available if Enthought Distribution is installed:
# http://www.enthought.com/products/epd_free.php

# Otherwise, download and install individually based on what
# version of Python you have, for Windows users
# typically something like 'package-version-python2.x.exe 

import sys  

passed = True

print 'Making a quick check for Python packages used in class:\n'
#print '\tsys.platform = %s' % sys.platform
print '\tPython version %s' % sys.version.split(' ')[0]

try:
    import numpy 
    print '\tNumPy version %s' % numpy.__version__
except:
    passed = False
    print '\tMISSING: NumPy'
    print '\t(check http://sourceforge.net/projects/numpy/files/NumPy/1.6.2/)'


try: 
    import matplotlib
    print '\tmatplotlib ver. %s' % matplotlib.__version__
except:
    passed = False
    print '\tMISSING: Matplotlib.'
    print '\t(check http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.0/)'


try:    
    import Image      
    print '\tImage version %s' % Image.VERSION
except:
    passed = False
    print '\tMISSING: Python image library (PIL)'
    print '\t(check http://www.pythonware.com/products/pil/#pil117)'
    
if passed:
    print '\nYou are good to go! See you in class.'
else:
    print '\nONE OR MORE PACKAGES MISSING.'
    print 'Please download and install the appropriate'
    print 'package for your Python version.'
    print 'Contact Ken (5-7844) if you have any trouble!'

raw_input('\n\nHit [Enter] to exit.')
    
