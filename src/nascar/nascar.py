import requests
import time
import logging

logger = logging.getLogger(__name__)

# verify this endpoint
API = "http://cf.nascar.com/live/feeds/lap-times.json"
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
        for lap in laps_json:
            self.laps.append(Lap(lap["Lap"], lap["LapTime"], lap["RunningPos"]))

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

    def update_lap_times(self, laps_json):
        old_laps = set(self.laps.laps)
        updated_laps = set(Laps(laps_json).laps)
        new_laps = updated_laps.difference(old_laps)
        for lap in new_laps:
            logger.info(f"Driver: {self.name}, {str(lap)}")

        self.laps.add_laps(new_laps)


class Drivers:
    def __init__(self, laps):
        self.drivers = self.parse_drivers(laps)

    def parse_driver(self, driver):
        driver_id = driver["NASCARDriverID"]
        return {
            driver_id: Driver(
                driver["Number"], driver["FullName"], driver["Manufacturer"], driver_id
            )
        }

    def parse_drivers(self, laps):
        drivers = {}
        for driver in laps:
            drivers.update(self.parse_driver(driver))
        return drivers

    def update_lap_times(self, laps_json):
        for driver_json in laps_json:
            self.drivers[driver_json["NASCARDriverID"]].update_lap_times(
                driver_json["Laps"]
            )
            pass


def get_lap_data():
    # call API endpoint
    res = requests.get(API)
    return res.json()
    pass


def main():
    while True:
        print("Hi my name is: !")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    # use loop here waiting for race to start
    data = get_lap_data()
    #
    drivers = Drivers(data["laps"])
    main()
