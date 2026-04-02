import psycopg2
from psycopg2 import Error

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
    running=False
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
    pass
run=True
while run:
    print()
    a=input()

    if a=='a':
        b=input()
        c = """
        CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
        RETURNS TABLE(name TEXT, phone TEXT) AS $$
        BEGIN
            RETURN QUERY
            SELECT c.name, c.phone
            FROM phonebook c
            WHERE c.name ILIKE '%' || p || '%'
            OR c.phone ILIKE '%' || p || '%';
        END;
        $$ LANGUAGE plpgsql;
        """
        cursor.execute(c)
        connect.commit()
        cursor.execute("SELECT * FROM get_contacts_by_pattern(%s);",(b,))
        row=cursor.fetchall()
        for i in row:
            print(i)
    elif a=='b':
            b,s=map(str,input().split())
            c='''
        CREATE OR REPLACE PROCEDURE update_or_into(p_name TEXT,p_phone TEXT)
        LANGUAGE plpgsql AS $$
        BEGIN
            IF EXISTS(SELECT 1 FROM phonebook WHERE name=p_name) THEN
            UPDATE phonebook SET phone=p_phone WHERE name=p_name;
        ELSE 
            INSERT INTO phonebook(name,phone) VALUES (p_name,p_phone);
        END IF;
        END;
        $$;
            '''
            cursor.execute(c)
            connect.commit()
            cursor.execute("CALL update_or_into(%s,%s);",(b,s))
    elif a=='c':
        names=list(map(str,input().split()))
        phones=list(map(str,input().split()))
        c='''CREATE OR REPLACE PROCEDURE insert_users_with_validation(
            p_names TEXT[], 
            p_phones TEXT[]
        )
        LANGUAGE plpgsql
        AS $$
        DECLARE
            i INTEGER;
            current_name TEXT;
            current_phone TEXT;
            phone_regex TEXT := '^\\+?[0-9]{10,12}$'; 
        BEGIN
            FOR i IN 1..cardinality(p_names) LOOP
                current_name := p_names[i];
                current_phone := p_phones[i];
                IF current_phone ~ phone_regex THEN
                    -- Если номер верный, вставляем в таблицу
                    INSERT INTO phonebook (name, phone) 
                    VALUES (current_name, current_phone);
                    RAISE NOTICE 'Контакт % добавлен успешно.', current_name;
                ELSE
                    RAISE WARNING 'Некорректный номер для пользователя %: %', current_name, current_phone;
                END IF;
            END LOOP;
        END;
        $$;'''
        cursor.execute(c)
        connect.commit()
        cursor.execute("CALL insert_users_with_validation(%s,%s);",(names,phones))
    elif a=='d':
        c='''
            CREATE OR REPLACE FUNCTION select_limits(
            limits INTEGER, offsets INTEGER)
            RETURNS TABLE(name TEXT, phone TEXT) AS $$
            BEGIN 
                RETURN QUERY 
                SELECT * FROM phonebook
                ORDER BY id
                LIMIT limits
                OFFSET offsets;
            END;
            && LANGUAGE plpgsql;'''
        cursor.execute(c)
        connect.commit()
        b=list(map(str,input('Limit and Offset:').split()))
        cursor.execute("SELECT * FROM select_limits(%s,%s);",(b[0],b[1]))
    elif a=='e':
        c='''CREATE OR REPLACE PROCEDURE delete_person(p_name_phone TEXT)
        LANGUAGE plpgsql AS $$
        BEGIN 
            IF EXISTS (SELECT 1 FROM phonebook WHERE name=p_name_phone OR phone=p_name_phone)THEN 
                DELETE FROM phonebook WHERE name=p_name_phone OR phone=p_name_phone;
                RAISE NOTICE 'Удаленно!';
            ELSE RAISE WARNING 'НЕПРАВИЛЬНО!!';
            END IF;
        END;
        $$;
        '''
        cursor.execute(c)
        connect.commit()
        b=input('Name or phone')
        cursor.execute('CALL delete_person(%s);',(b,))
        print(connect.notices[0])
            
    elif a=='q':
        run=False
    connect.commit()
    
if connect:
    connect.commit()
    cursor.close()
    connect.close()
    print('закрыто')