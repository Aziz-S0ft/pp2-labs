import math
#Task N1
n=int(input())
print(f'{math.radians(n):.6f}')
#Task N2
h=int(input())
fvalue=int(input())
svalue=int(input())
print((fvalue+svalue)/2*h)
#Task N3
s=int(input())
l=int(input())
gr=(math.pi*(s-2))/s
x=(l*math.sin((math.pi-gr)/2))/math.sin(gr)
print(math.ceil(s*(1/2)*x*x*math.sin(gr)))
#Task N4
l=int(input())
h=int(input())
print(l*h)