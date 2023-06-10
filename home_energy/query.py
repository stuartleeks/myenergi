import sqlite3

def main():
    conn = sqlite3.connect('home_energy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date(date) as date, SUM(imported)/(3600*1000) as imported, SUM(exported)/(3600*1000) as exported FROM energy GROUP by date(date)")
    res = cursor.fetchall()
    print(res)


if __name__ == "__main__":
    main()