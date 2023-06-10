import sqlite3

def main():
    conn = sqlite3.connect('home_energy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date(date) as date, SUM(imported)/(3600*1000) as imported, SUM(exported)/(3600*1000) as exported FROM energy GROUP by date(date)")
    res = cursor.fetchall()
    for item in res:
        print(item)

    print()
    print("=====================")
    print()

    cursor.execute("SELECT date(date) as date, COUNT(*) as count FROM energy GROUP by date(date)")
    res = cursor.fetchall()
    for item in res:
        print(item)

    print()
    print("=====================")
    print()

    cursor.execute("SELECT date(date) as date, MAX(date) as max FROM energy GROUP by date(date)")
    res = cursor.fetchall()
    for item in res:
        print(item)

if __name__ == "__main__":
    main()