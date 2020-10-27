from collections import namedtuple
import typing
import threading
import asyncio
import time
import struct

import RN4870 as ble_module

handle_table = {
    '0094': 'lat',
    '0096': 'lon',
    '009A': 'elev',
    '0098': 'speed',
    '0092': 'heart_rate'
}

WatchData = namedtuple('WatchData', "lat lon elev speed heart_rate")

# global variable to make access similar to threaded AGPS3 implemetation
Watch = WatchData(0.0, 0.0, 0.0, 0.0, 0.0)
counter = 0


async def main():
    await ble_module.open_connection()
    print("Watch code starts...")

    main_loop = asyncio.get_event_loop()
    main_loop.create_task(watch_thread())

    global counter
    while True:
        await asyncio.sleep(0)
        time.sleep(1)
        print(Watch.lat, Watch.lon, Watch.speed)
        print("Total packets received: " + str(counter))


async def watch_update() -> typing.Tuple[str, float]:
    handle, packet = await ble_module.rx_packet()
    numeric_value = float(int.from_bytes(packet, byteorder="little", signed=True))
    if handle is not "0092":
        numeric_value = numeric_value / 1000000
    return handle, numeric_value


async def watch_thread():
    global Watch
    global counter

    # keys in current_data are RN4871 handles, exact values TBD
    current_data = {
        '0094': 0.0,
        '0096': 0.0,
        '009A': 0.0,
        '0098': 0.0,
        '0092': 0.0
    }

    while True:
        handle, value = await watch_update()
        current_data[handle] = value
        Watch = WatchData(**{handle_table[handle]: current_data[handle] for handle in current_data.keys()})
        counter += 1


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main())
    finally:
        main_loop.close()
