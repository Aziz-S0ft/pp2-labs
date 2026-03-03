import re
with open("Lab5/raw.txt",'r') as f:
    a=f.read()
#Task N1
print(re.findall(r'ab*',a))
#Task N2
print(re.findall(r"ab{2,3}",a))
#Task N3
print(re.findall(r'[a-z]+_[a-z]+',a))
#Task N4
print(re.findall(r'[A-Z][a-z]+',a))
#Task N5
print(re.findall(r'a.*b',a))
#Task N6
print(re.sub(r',|\.| ',':',a))
#Task N7
print(re.sub(r'_([a-z])',lambda x:str(x.group(1)).upper(),a))
#Task N8
print('\n'.join(re.findall(r'[A-Z][a-z]*',a)))
#Task N9
print(' '.join(re.findall(r'[A-Z][a-z]*',a)))
#Task N10
print(re.sub(r'\B[A-Z]',lambda x:'_'+str(x.group()).lower(),a))