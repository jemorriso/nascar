import requests
import time
import logging
from sys import stdout
from datetime import datetime
import csv
import re
import json

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=stdout))

API = "http://racecontrol.indycar.com/xml/timingscoring.json"
INTERVAL = 5


class Lap:
    def __init__(self, number, time, position):
        self.number = number
        self.time = time
        self.position = position

    def __str__(self):
        return f"Lap number: {self.number}, Lap time: {self.time}, Driver position: {self.position}"  # noqa: E501


class Laps:
    def __init__(self, laps_json=None):
        self.laps = []
        if laps_json is not None:
            self.add_laps_json(laps_json)

    def add_laps_json(self, laps_json):
        # For IndyCar we just have access to the last lap time
        self.laps.append(
            Lap(laps_json["laps"], laps_json["lastLapTime"], laps_json["overallRank"])
        )

    def add_laps(self, laps):
        self.laps.extend(laps)


class Driver:
    def __init__(self, number, name, manufacturer, id):
        self.number = number
        self.name = name
        self.manufacturer = manufacturer
        self.id = id
        self.position = None
        self.laps = Laps()

    def last_lap():
        pass

    def get_new_laps(self, laps_json):
        old_laps = set(self.laps.laps)
        old_lap_numbers = set([lap.number for lap in old_laps])
        updated_laps = set(Laps(laps_json).laps)
        new_laps = [lap for lap in updated_laps if lap.number not in old_lap_numbers]
        for lap in new_laps:
            logger.info(f"Driver: {self.name}, {str(lap)}")
            print(f"Driver: {self.name}, {str(lap)}")

        return new_laps


class Drivers:
    def __init__(self, laps):
        self.drivers = self.parse_drivers(laps)

    def parse_driver(self, driver):
        driver_id = driver["DriverID"]
        driver_name = f"{driver['firstName']} {driver['lastName']}"
        return {
            driver_id: Driver(
                driver["EntrantID"], driver_name, driver["team"], driver_id
            )
        }

    def parse_drivers(self, items):
        drivers = {}
        for driver in items:
            drivers.update(self.parse_driver(driver))
        return drivers

    def update_lap_times(self, laps_json):
        drivers_new_laps = []
        for driver_json in laps_json:
            driver = self.drivers[driver_json["DriverID"]]
            new_laps = driver.get_new_laps(driver_json)
            driver.laps.add_laps(new_laps)
            drivers_new_laps.append((driver, new_laps))
        return drivers_new_laps


def transform_laps(driver_laps):
    dict_laps = []
    for driver, laps in driver_laps:
        for lap in laps:
            dict_laps.append(
                {
                    "Name": driver.name,
                    "Lap Number": lap.number,
                    "Running Position": lap.position,
                    "Lap Time": lap.time,
                }
            )
    return dict_laps


def init_csv(f, header_keys):
    writer = csv.DictWriter(f, fieldnames=header_keys)
    writer.writeheader()
    return writer


def append_csv(dict_laps, writer):
    writer.writerows(dict_laps)


def get_json(text):
    # Using greedy matching because I know I want the LAST closing parens to match, and
    # not any intermediate ones.
    json_text = re.search(r"\((.*)\)", text, flags=re.DOTALL).group(1)
    return json.loads(json_text)


def get_lap_data():
    res = requests.get(API)
    return get_json(res.text)


def main(drivers, writer):
    while True:
        data = get_lap_data()
        drivers_new_laps = drivers.update_lap_times(data["timing_results"]["Item"])
        if drivers_new_laps:
            dict_laps = transform_laps(drivers_new_laps)
            append_csv(dict_laps, writer)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    data = get_lap_data()
    fname = f"IndyCar-{datetime.now().date().isoformat()}.csv"
    drivers = Drivers(data["timing_results"]["Item"])
    with open(fname, "a") as f:
        writer = init_csv(f, [])
        main(drivers, writer)