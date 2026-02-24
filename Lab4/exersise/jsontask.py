import json
with open('sample-data.json','r') as file:
    global text
    text=json.load(file)
print(text)
text1=text['imdata']
print('Interface Status')
print('='*80)
print('DN',' '*41,'Description        Speed    MTU')
print('-'*44,'-'*18,'-'*8,'-'*5)
for i in text1:
    j=i["l1PhysIf"]["attributes"]
    print(j['dn'],end='            ')
    if 'description' in j:
        print(j['description'],end='      ')
    else:print(' '*10,end='')
    print(j['speed'],' ',j['mtu'])