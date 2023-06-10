import datetime
import os
from myenergi import MyEnergi
from dotenv import load_dotenv

import sqlite3

load_dotenv(dotenv_path="../.env")


def main():
    serial_number = os.getenv("SERIAL_NUMBER", None)
    api_key = os.getenv("API_KEY", None)

    if not serial_number:
        raise ValueError("SERIAL_NUMBER not set")

    if not api_key:
        raise ValueError("API_KEY not set")
    
    with sqlite3.connect('home_energy.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS energy (date text, imported real, exported real, generated real, zappi real, self_consumption real, usage real, property_usage real, voltage real, frequency real, PRIMARY KEY (date))")

        myenergi = MyEnergi(api_key, serial_number)
        print("Date, Imported, Exported, Generated, Zappi, Usage")

        date = datetime.date(2023, 3, 1)
        for i in range(0, 31 + 30 +31 +8):
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