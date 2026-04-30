import psycopg2
import json
import csv

# ---------------- CONNECTION ----------------
conn = psycopg2.connect(
        user="aziz",
        password="1234",
        host="127.0.0.1",
        port="5432",
        database="kbtu"
)
cur = conn.cursor()

def import_csv():
    with open("contacts.csv", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group_name"]
            phone = row["phone"]
            phone_type = row["type"]

            # проверка дубликатов
            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists. skip / overwrite: ")
                if choice == "skip":
                    continue
                else:
                    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            # вставка группы
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group_name,))

            cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
            group_id = cur.fetchone()[0]

            # вставка контакта
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            # вставка телефона
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, phone_type))

        conn.commit()
        print("CSV imported successfully")
# ---------------- FILTER ----------------
def filter_by_group():
    group_name = input("Group name: ")

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group_name,))

    for row in cur.fetchall():
        print(row)

# ---------------- SEARCH EMAIL ----------------
def search_email():
    query = input("Email search: ")

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s
    """, ('%' + query + '%',))

    print(cur.fetchall())

# ---------------- SEARCH ALL (FUNCTION) ----------------
def search_all():
    query = input("Search (name/email/phone): ")

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    print(cur.fetchall())

# ---------------- SORT ----------------
def sort_contacts():
    allowed = ["name", "birthday", "created_at"]
    field = input("Sort by (name/birthday/created_at): ")

    if field not in allowed:
        print("Invalid field")
        return

    cur.execute(f"""
        SELECT name, birthday, created_at
        FROM contacts
        ORDER BY {field}
    """)

    print(cur.fetchall())

# ---------------- PAGINATION ----------------
def paginate(limit=3):
    offset = 0

    while True:
        cur.execute("""
            SELECT name FROM contacts
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()
        print(rows)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

# ---------------- EXPORT JSON ----------------
def export_json():
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]),
            "group": r[3],
            "phone": r[4],
            "type": r[5]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported to contacts.json")

# ---------------- IMPORT JSON ----------------
def import_json():
    with open("contacts.json", "r") as f:
        data = json.load(f)

    for row in data:
        name = row["name"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip / overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        # group
        cur.execute("""
            INSERT INTO groups(name)
            VALUES (%s)
            ON CONFLICT DO NOTHING
        """, (row["group"],))

        cur.execute("SELECT id FROM groups WHERE name=%s", (row["group"],))
        group_id = cur.fetchone()[0]

        # contact
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (row["name"], row["email"], row["birthday"], group_id))

        contact_id = cur.fetchone()[0]

        # phone
        if row["phone"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, row["phone"], row["type"]))

    conn.commit()
    print("Imported from JSON")

# ---------------- PROCEDURE: ADD PHONE ----------------
def add_phone_proc():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()

    print("Phone added")

# ---------------- PROCEDURE: MOVE GROUP ----------------
def move_group_proc():
    name = input("Contact name: ")
    group = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()

    print("Group updated")

# ---------------- MENU ----------------
def menu():
    while True:
        print("\n====== PHONEBOOK ======")
        print("1. Filter by group")
        print("2. Search by email")
        print("3. Search all")
        print("4. Sort contacts")
        print("5. Pagination")
        print("6. Export JSON")
        print("7. Import JSON")
        print("8. Add phone (procedure)")
        print("9. Move to group (procedure)")
        print("10. Import CSV")
        print("0. Exit")

        choice = input(">> ")

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_email()
        elif choice == "3":
            search_all()
        elif choice == "4":
            sort_contacts()
        elif choice == "5":
            paginate()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            add_phone_proc()
        elif choice == "9":
            move_group_proc()
        elif choice == "10":
            import_csv()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

    conn.close()

# ---------------- START ----------------
menu()