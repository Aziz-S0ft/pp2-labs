def count_up(n):
    for i in range(1,n+1):
        yield i
a=int(input())
for i in count_up(a):
    print(i)