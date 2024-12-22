import os, re 

def find_python_files(path):
    return [one_file_name.replace('.py','') for one_file_name in os.listdir(os.path.abspath(path)) if one_file_name != '__init__.py' and re.match(r'.*\.py$',one_file_name) is not None]

for each_file in find_python_files(path=os.path.dirname(__file__)):
    exec('from .'+each_file+' import *')