import datetime
import os
from myenergi import MyEnergi
from dotenv import load_dotenv

import sqlite3

load_dotenv(dotenv_path="../.env")

database_path = os.getenv("DATABASE_PATH", "./home_energy.db")
default_start_date = os.getenv("DEFAULT_START_DATE", "")

def main():
    serial_number = os.getenv("SERIAL_NUMBER", None)
    api_key = os.getenv("API_KEY", None)

    if not serial_number:
        raise ValueError("SERIAL_NUMBER not set")

    if not api_key:
        raise ValueError("API_KEY not set")
    
    db_file = os.path.abspath(database_path)
    print("db_file: ", db_file)
    db_path = os.path.dirname(db_file)
    print("db_path: ", db_path)
    if not os.path.exists(db_path):
        print(f"Creating database directory: '{db_path}'")
        os.makedirs(db_path)
    db_path_stat = os.stat(db_path)
    print ("db path mode: ", oct(db_path_stat.st_mode))

    print(f"Opening database: '{database_path}'")
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS energy (date text, imported real, exported real, generated real, zappi real, self_consumption real, usage real, property_usage real, voltage real, frequency real, PRIMARY KEY (date))")
        conn.commit()

        cursor.execute("SELECT MAX(date) FROM energy")
        res = cursor.fetchall()
        max_date= res[0][0]
        print(f"Max date: {max_date}")

        if max_date is None:
            # no data - use default start date
            if default_start_date:
                start_date = datetime.datetime.strptime(default_start_date, '%Y-%m-%d').date()
            else:
                start_date = datetime.date.today()
        else:
            max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')
            if max_date.hour == 23 and max_date.minute == 59:
                # Have all of latest day's data - advance a day
                start_date = max_date.date() + datetime.timedelta(days=1)
            else:
                # Still have data to collect for specified day
                start_date = max_date.date()

        myenergi = MyEnergi(api_key, serial_number)
        print("Date, Imported, Exported, Generated, Zappi, Usage")

        date = start_date
        while date <= datetime.date.today():
            day_data = myenergi.get_day_data(date=date)
            imported = 0
            exported = 0
            generated = 0
            zappi = 0
            usage = 0
            for item in day_data:
                imported += item.imported
                exported += item.exported
                generated += item.generated
                zappi += item.zappi
                usage += item.usage
                cursor.execute("INSERT OR IGNORE INTO energy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item.time, item.imported, item.exported, item.generated, item.zappi, item.self_consumption, item.usage, item.property_usage, item.voltage, item.frequency))

            imported = imported / (3600 * 1000)
            exported = exported / (3600 * 1000)
            generated = generated / (3600 * 1000)
            zappi = zappi / (3600 * 1000)
            usage = usage / (3600 * 1000)
            print(f"{item.time.date()}, {imported: 0.1f}, {exported: 0.1f}, {generated: 0.1f}, {zappi: 0.1f}, {usage: 0.1f}")
    
            date = date + datetime.timedelta(days=1)
            conn.commit()


if __name__ == "__main__":
    main()