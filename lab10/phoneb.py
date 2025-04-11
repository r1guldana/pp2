import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="thismysql2025forpp2", 
        host="localhost",
        port="5432"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_manual():
    name = input("input name ")
    phone = input("input phone ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("new user added")

# 2. Загрузка из CSV
def insert_from_csv():
    filename = input("input CSV-file <<database.csv>>: ")
    try:
        conn = connect()
        cur = conn.cursor()
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row['name'], row['phone']))
        conn.commit()
        cur.close()
        conn.close()
        print("csv datas added.")
    except Exception as e:
        print("error", e)

# 3. Обновление данных
def update_user():
    field = input("choose what you want update 1 or 2 :")
    if field == "1":
        old_name = input("input current name:")
        new_name = input("input new name:")
        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, old_name))
    elif field == "2":
        old_phone = input("input current phone: ")
        new_phone = input("input new phone: ")
        conn = connect()
        cur = conn.cursor()
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
    else:
        print("error")
        return
    conn.commit()
    cur.close()
    conn.close()
    print("datas updated")

# 4. Поиск по имени или номеру
def search_user():
    key = input("search user 1 or 2 ")
    conn = connect()
    cur = conn.cursor()
    if key == "1":
        name = input("input name: ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
    elif key == "2":
        phone = input("input phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f"%{phone}%",))
    else:
        print("errorer")
        return
    results = cur.fetchall()
    for row in results:
        print(row)
    cur.close()
    conn.close()

# 5. Удаление пользователя
def delete_user():
    key = input("delete 1 or 2: ")
    conn = connect()
    cur = conn.cursor()
    if key == "1":
        name = input("input name: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif key == "2":
        phone = input("input phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("error")
        return
    conn.commit()
    cur.close()
    conn.close()
    print("user daleted")

# 6. Показать всю таблицу
def show_all():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Меню
def menu():
    create_table()
    while True:
        print("\nphone book:")
        print("1. insert")
        print("2. insert in CSV")
        print("3. update name and phone")
        print("4. search user")
        print("5. delete user")
        print("6. show all")
        print("0. exit")

        choice = input("Выберите действие: ")

        if choice == "1":
            insert_manual()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_user()
        elif choice == "4":
            search_user()
        elif choice == "5":
            delete_user()
        elif choice == "6":
            show_all()
        elif choice == "0":
            print("👋 bye!")
            break
        else:
            print("error")

# Запуск
if __name__ == "__main__":
    menu()
