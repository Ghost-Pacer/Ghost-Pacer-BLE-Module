from collections import namedtuple
import typing
import threading
import time

import RN4870 as ble_module

handle_table = {
    '0073': 'lat',
    '0075': 'lon',
    '0077': 'elev',
    '0079': 'speed',
    '0081': 'heart_rate'
}

WatchData = namedtuple('WatchData', "lat lon elev speed heart_rate")

# global variable to make access similar to threaded AGPS3 implemetation
Watch: WatchData = WatchData(0.0, 0.0, 0.0, 0.0, 0.0)


async def watch_update() -> typing.Tuple[str, float]:
    handle, packet = ble_module.rx_packet()
    numeric_value = float(packet.decode("ascii"))
    return handle, numeric_value


def watch_thread():
    global Watch

    # keys in current_data are RN4871 handles, exact values TBD
    current_data = {
        '0073': 0.0,  # lat
        '0075': 0.0,  # lon
        '0077': 0.0,  # elev
        '0079': 0.0,  # speed
        '0081': 0.0  # heart rate
    }

    while True:
        handle, value = await watch_update()
        current_data[handle] = value
        Watch = WatchData(**{handle_table[handle]: current_data[handle] for handle in current_data.keys()})


# Intended Use
# threading.Thread(target=watch_thread).start()
# while True:
#     time.sleep(1)
#     print(Watch.lat, Watch.lon, Watch.speed)
