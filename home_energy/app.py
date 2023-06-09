import datetime
import os
from myenergi import MyEnergi
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")


def main():
    serial_number = os.getenv("SERIAL_NUMBER", None)
    api_key = os.getenv("API_KEY", None)

    if not serial_number:
        raise ValueError("SERIAL_NUMBER not set")

    if not api_key:
        raise ValueError("API_KEY not set")

    myenergi = MyEnergi(api_key, serial_number)
    print("Date, Imported, Exported, Generated, Zappi, Usage")

    date = datetime.date(2023, 5, 1)
    for i in range(0, 10):
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

        imported = imported / (3600 * 1000)
        exported = exported / (3600 * 1000)
        generated = generated / (3600 * 1000)
        zappi = zappi / (3600 * 1000)
        usage = usage / (3600 * 1000)
        print(f"{item.time.date()}, {imported: 0.1f}, {exported: 0.1f}, {generated: 0.1f}, {zappi: 0.1f}, {usage: 0.1f}")
        date = date + datetime.timedelta(days=1)

if __name__ == "__main__":
    main()