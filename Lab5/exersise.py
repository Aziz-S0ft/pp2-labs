import re
with open("Lab5/raw.txt",'r') as f:
    a=f.read()
#Task N1
t1=re.findall(r'Стоимость\n([\d, ]+)\n',a)
print(t1)
#Task N2
t2=re.findall(r'\d+\.\n(.+?)\n\d+[, ]*\d*\s*x',a)
print(t2)
#Task N3
t3=re.search(r'ИТОГО:\n([\d ,]+)',a).group(1)
print(t3)
#Task N4
t4=re.search(r'Время: ([\d \.:]+)\n',a).group(1)
print(t4)
#Task N5
t5=' , '.join(re.findall(r'Банковская карта|Наличные|Электронный кошелёк',a))
print(t5)
#task N6
t6={};ts6=[t4,t5,'',t3];tts6=['дата_время','способ_оплаты','товары',"итого"]
for i in range(len(ts6)):
    t6[tts6[i]]=ts6[i]
m=[]
for i in range(len(t2)):
    m.append({"название": t2[i], "цена": t1[i]})
t6['товары']=m
print(t6)