import os
if os.name == 'nt':
    from windows import *
elif os.name == 'posix':
    from linux import *