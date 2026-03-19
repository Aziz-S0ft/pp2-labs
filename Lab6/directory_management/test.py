import shutil
import os
print(os.getcwd())
a='Edjuge_labs/lab9/pygme.py'
b='pp2-labs/lab9'
os.makedirs(b,exist_ok=True)
b+='/'
if os.path.exists(a):
    shutil.copy(a,b)
    print('good')