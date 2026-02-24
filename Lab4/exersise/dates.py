from datetime import datetime ,timedelta
#Task N1
'''a=input()
b=datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
s=b-timedelta(5)
print(s)
#Task N2
a=datetime.now()
print('Yesterday',a-timedelta(1))
print('Today',a)
print('Tomorrow',a+timedelta(1))
#Task N3
a=datetime.now()
print(a-timedelta(microseconds=a.microsecond))'''
#Task N4
a=input()
b=input()
a=datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
b=datetime.strptime(b,'%Y-%m-%d %H:%M:%S')
s=a-b
print(int(s.total_seconds()))