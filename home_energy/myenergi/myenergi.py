import datetime
from requests.auth import HTTPDigestAuth

import requests

server = "s18"


class DataPerMinuteItem:
    """Class to represent data with a per-minute granularity"""

    _time: datetime.datetime
    _imported: int
    _exported: int
    _generated: int
    _zappi: int
    _voltage: int
    _frequency: int

    def __init__(
        self,
        time: datetime.datetime,
        imported: int,
        exported: int,
        generated: int,
        zappi: int,
        voltage: int,
        frequency: int,
    ):
        self._time = time
        self._imported = imported
        self._exported = exported
        self._generated = generated
        self._zappi = zappi
        self._voltage = voltage
        self._frequency = frequency

    def from_dict(data: dict) -> "DataPerMinuteItem":
        year = data["yr"]
        month = data["mon"]
        day = data["dom"]
        hour = data.get("hr", 0)
        minute = data.get("min", 0)
        time = datetime.datetime(year, month, day, hour, minute)
        imported = data.get("imp", 0)
        exported = data.get("exp", 0)
        generated = data.get("gep", 0)
        h1d = data.get("h1d", 0)
        h2d = data.get("h2d", 0)
        h3d = data.get("h3d", 0)
        h1b = data.get("h1b", 0)
        h2b = data.get("h2b", 0)
        h3b = data.get("h3b", 0)
        zappi = h1d + h2d + h3d + h1b + h2b + h3b
        voltage = data.get("v1", 0)
        frequency = data.get("frq", 0)

        return DataPerMinuteItem(
            time, imported, exported, generated, zappi, voltage, frequency
        )
    
    def __repr__(self) -> str:
        return f"DataPerMinuteItem({self._time}, {self._imported}, {self._exported}, {self._generated}, {self._zappi}, {self._voltage}, {self._frequency})"

    @property
    def time(self) -> datetime.datetime:
        return self._time
    
    @property
    def imported(self) -> int:
        """Imported energy in J"""
        return self._imported
    
    @property
    def exported(self) -> int:
        """Exported energy in J"""
        return self._exported
    
    @property
    def generated(self) -> int:
        """Generated energy in J"""
        return self._generated
    
    @property
    def zappi(self) -> int:
        """Zappi energy in J"""
        return self._zappi
    
    @property
    def voltage(self) -> int:
        """Voltage in decaVolts"""
        return self._voltage
    
    @property
    def frequency(self) -> int:
        """Frequency in centaHertz"""
        return self._frequency

    @property
    def self_consumption(self) -> int:
        """Self consumption in J"""
        return self._generated - self._exported
    
    @property
    def usage(self) -> int:
        """Overall usage in J"""
        return self._imported + self.self_consumption
    
    @property
    def property_usage(self) -> int:
        """Property usage in J (excl Zappi)"""
        return self.usage - self._zappi



class MyEnergi:
    """Class to interact with myenergi API"""

    _api_key: str
    _serial_number: str
    _id: str

    def __init__(self, api_key: str, serial_number: str):
        self._api_key = api_key
        self._serial_number = serial_number
        self._id = "Z" + serial_number

    def get_day_data(self, date: datetime.date) -> list[DataPerMinuteItem]:
        year = date.year
        month = date.month
        day = date.day
        url = f"https://{server}.myenergi.net/cgi-jday-{self._id}-{year}-{month}-{day}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        r = requests.get(
            url,
            auth=HTTPDigestAuth(self._serial_number, self._api_key),
            headers=headers,
            timeout=20,
        )

        r.raise_for_status()

        response_json = r.json()
        data = response_json[f"U{self._serial_number}"]

        return [DataPerMinuteItem.from_dict(item) for item in data]
