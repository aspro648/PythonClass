
import os, sys

base_dir = os.getcwd()

dirs_to_kill = ['graphs', 'images', 'propertyTables']

for (path, dirs, files) in os.walk(os.path.join(base_dir, 'sim3134')):
    print 'path = %s' % path
    print 'dirs = %s' % dirs
    print 'files = %s' % files
    print '\n'
    if dirs:
        for dirName in dirs:
            if dirName in dirs_to_kill:
                os.removedirs(os.path.join(path, dirName))

                #os.system('remove %s' % os.path.join(path, dirName))
                
                
            
    
