import psycopg2
import csv
from io import StringIO
from psycopg2 import Error
with open ("data.csv","r") as f:
    dats=f.read()
r = csv.reader(StringIO(dats))
connect=None
try:
    connect=psycopg2.connect(
        user="aziz",
        password="1234",
        host="127.0.0.1",
        port="5432",
        database="kbtu"
    )
    cursor = connect.cursor()
    for i in r:
        cursor.execute(f"INSERT INTO phonebook (name, phone) VALUES ('{i[0]}','{i[1]}');")
    running=True
    while running:
        print('Выход:\\q \nТаблица:\\tab \nИзменить номер:\\update \nДобавит человека \\add \nУдалит человека \\del: \nПоиск по Именам:\\query')
        a=input()
        if a=='\\q':running=False
        elif a=='\\update':
            b=input('пишите имя и новый номер:');b=list(b.split())
            cursor.execute(f"UPDATE phonebook SET phone = '{b[1]}' WHERE Name = '{b[0]}';")
        elif a=='\\tab':
            cursor.execute("SELECT * FROM phonebook;")
            rows=cursor.fetchall()
            for i in rows:
                print(f"Name: {i[1]} | Phone: {i[2]} ")
        elif a=='\\add':
            a=input('Имя и номер:')
            b=a.split()
            cursor.execute(f"INSERT INTO phonebook (name,phone) VALUES ('{b[0]}','{b[1]}');")
        elif a=='\\del':
            b=input('Пишите Имя:')
            cursor.execute(f"DELETE FROM phonebook WHERE Name = '{b}';")
        elif a=='\\query':
            b=input('Пишите поиск:')
            cursor.execute(f"SELECT * FROM phonebook WHERE Name LIKE '%{b}%';")
            rows=cursor.fetchall()
            for i in rows:
                print(f"Name: {i[1]} | Phone: {i[2]} ")
        else:print('Неизветный команда пишите снова!')
            
        
except (Exception,Error) as error:
    print("Ошибка при работе с PostgreSQL:",Error)
finally:
    if connect:
        connect.commit()
        cursor.close()
        connect.close()
        print('закрыто')