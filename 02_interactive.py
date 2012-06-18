# Example interative session exploring enviroment
# (saved as .py for color highlighting)

>>> help

>>> help()

>>> help(dir)
Help on built-in function dir in module __builtin__:

dir(...)
    dir([object]) -> list of strings
    
    Return an alphabetized list of names comprising (some of) the attributes
    of the given object, and of attributes reachable from it:
    
    No argument:  the names in the current scope.
    Module object:  the module attributes.
    Type or class object:  its attributes, and recursively the attributes of
        its bases.
    Otherwise:  its attributes, its class's attributes, and recursively the
        attributes of its class's base classes.
        
>>> dir()
['Image', '__builtins__', '__doc__', '__name__', '__warningregistry__', 'cwd', 
 'matplotlib', 'numpy', 'os', 'printVersions', 'sys']

>>> dir(os)
['F_OK', 'O_APPEND', 'O_BINARY', 'O_CREAT', 'O_EXCL', 'O_NOINHERIT', 'O_RANDOM', 
 'O_RDONLY', 'O_RDWR', 'O_SEQUENTIAL', 'O_SHORT_LIVED', 'O_TEMPORARY', 'O_TEXT', 
 'O_TRUNC', 'O_WRONLY', 'P_DETACH', 'P_NOWAIT', 'P_NOWAITO', 'P_OVERLAY', 'P_WAIT', 
 'R_OK', 'SEEK_CUR', 'SEEK_END', 'SEEK_SET', 'TMP_MAX', 'UserDict', 'W_OK', 'X_OK', 
 '_Environ', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '_copy_reg', 
 '_execvpe', '_exists', '_exit', '_get_exports_list', '_make_stat_result', 
 '_make_statvfs_result', '_pickle_stat_result', '_pickle_statvfs_result', 'abort', 
 'access', 'altsep', 'chdir', 'chmod', 'close', 'curdir', 'defpath', 'devnull', 'dup', 
 'dup2', 'environ', 'errno', 'error', 'execl', 'execle', 'execlp', 'execlpe', 'execv', 
 'execve', 'execvp', 'execvpe', 'extsep', 'fdopen', 'fstat', 'fsync', 'getcwd', 'getcwdu', 
 'getenv', 'getpid', 'isatty', 'linesep', 'dir_list', 'lseek', 'lstat', 'makedirs', 'mkdir', 
 'name', 'open', 'pardir', 'path', 'pathsep', 'pipe', 'popen', 'popen2', 'popen3', 'popen4', 
 'putenv', 'read', 'remove', 'removedirs', 'rename', 'renames', 'rmdir', 'sep', 'spawnl', 
 'spawnle', 'spawnv', 'spawnve', 'startfile', 'stat', 'stat_float_times', 'stat_result', 
 'statvfs_result', 'strerror', 'sys', 'system', 'tempnam', 'times', 'tmpfile', 'tmpnam', 
 'umask', 'unlink', 'unsetenv', 'urandom', 'utime', 'waitpid', 'walk', 'write']

>>> help(os.getcwd)
Help on built-in function getcwd in module nt:

getcwd(...)
    getcwd() -> path
    
    Return a string representing the current working directory.
    
>>> os.getcwd()
'C:\\Windows\\system32'

>>> os.chdir('C:\Users\kennetho\Documents\PythonClass2')
>>> os.getcwd()
'C:\\Users\\kennetho\\Documents\\PythonClass2'

>>> base_dir = os.getcwd()
>>> print base_dir
C:\\Users\\kennetho\\Documents\\PythonClass2

>>> os.listdir(base_dir)
['data_extraction.py', 'outline.txt', 'output.txt', 'sim1517']

>>> dir_list = os.listdir(base_dir)

>>> type(dir_list)
<type 'list'>

>>> type(os.listdir)
<type 'builtin_function_or_method'>

>>> for item in dir_list:
	print item
	
data_extraction.py
outline.txt
output.txt
sim1517

>>> for id, item in enumerate(dir_list):
	print id, item
	
0 data_extraction.py
1 outline.txt
2 output.txt
3 sim1517

>>> dir_list[3]
'sim1517'
>>> dir_list[-1]
'sim1517'
>>> dir_list[1:2]
['outline.txt']
>>> dir_list[1:3]
['outline.txt', 'output.txt']

>>> os.chdir(dir_list[3])
>>> os.getcwd()
'C:\\Users\\kennetho\\Documents\\PythonClass2\\sim1517'
>>> os.listdir(os.getcwd())
['arch_info.txt', 'eab5ad0667e7c3793842116c0d3a0e0f', 'easastatus.txt', 
 'easa_notes_UTF_8.txt', 'f14c081d66a26e2d8fece9ede931b400', 'files', 'GuiConfig.ccl', 
 'lr0', 'lr1', 'lr10', 'lr11', 'lr12', 'lr13', 'lr14', 'lr15', 'lr16', 'lr17', 'lr18', 
 'lr19', 'lr2', 'lr20', 'lr21', 'lr22', 'lr23', 'lr24', 'lr3', 'lr4', 'lr5', 'lr6', 
 'lr7', 'lr8', 'lr9']

>>> target_dir = 'sim1517'
>>> full_dir = os.path.join(base_dir, target_dir)
>>> full_dir
'C:\\Users\\kennetho\\Documents\\PythonClass2\\sim1517'
>>> os.path.basename(full_dir)
'sim1517'
>>> os.path.split(full_dir)
('C:\\Users\\kennetho\\Documents\\PythonClass2', 'sim1517')
>>> type(os.path.split(full_dir))
<type 'tuple'>

>>> os.path.split(full_dir)[0]
'C:\\Users\\kennetho\\Documents\\PythonClass2'
>>> os.path.split(full_dir)[1]
'sim1517

>>> os.path.exists(os.path.join(full_dir, 'easastatus.txt'))
True

>>> os.path.isfile(os.path.join(full_dir, 'easastatus.txt'))
True
>>> os.path.isdir(os.path.join(full_dir, 'easastatus.txt'))
False

>>> for (path, dirs, files) in os.walk(os.path.join(full_dir, 'lr0')):
	print 'path = %s' % path
	print 'dirs = %s' % dirs
	print 'files = %s' % files
	print '\n'
    
>>> file_obj = open(os.path.join(full_dir, 'lr0', 'vapor.inp'), 'r')
>>> content = file_obj.read()
>>> print content

>>> line = file_obj.readline()
>>> print line
'LINE 1 TITLE\n'
>>> line = file_obj.readline()
>>> print line
'400fpm, 13in, 20gsm, 90% water, SBS 9pt, 236um, optARN - 16ft - upto 200C.\n'
>>> line = file_obj.readline(2)
>>> line
'LI'
>>> line = file_obj.readline(2)
>>> line
'NE'

>>> lines = file_obj.readlines()
>>> type(lines)
>>> print lines
>>> for line in lines:
        print line
        
>>> for ln, line in enumerate(lines):
        print ln, line,
        
>>> lines = file_obj.readlines()
>>> print lines
[]

>>> file_obj.seek(0)
>>> lines = file_obj.readlines()
>>> print lines

>>> outFile = open(os.join(full_dir, 'outFile.txt'), 'w')
>>> outFile.write('This is my file')
>>> outFile.flush()
>>> outFile.write('Still my file')
>>> outFile.flush()
>>> outFile.write('\nEnought of this!\n')
>>> outFile.close()






