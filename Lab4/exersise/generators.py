#Task N1
n=int(input())
gen=(x*x for x in range(n))
for i in gen:
    print(i,end=' ')
print()
#Task N2
def gnr(a):
    for i in range(0,a,2):yield i
a=int(input())
a=gnr(a)
for i in a:print(i,end=' ')
print()
del gnr
#Task N3
def gnr(a):
    for i in range(0,a): 
        if i%3 and i%4:yield i
a=int(input())
a=gnr(a)
for i in a:print(i,end=' ')
del gnr
#Task N4
def squares(a,b):
    for i in range(a,b):yield i
a,b=map(int,input().split())
c=squares(a,b)
for i in c:print(i,end=' ')
#Task N4
def gnr(a):
    for i in range(a,-1,-1):yield i
a=int(input())
a=gnr(a)
for i in a:print(i,end=' ')