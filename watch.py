from collections import namedtuple
import typing
import threading
import asyncio
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
counter = 1


def main():
    print("hi")
    threading.Thread(target=watch_thread).start()

    global counter
    while True:
        time.sleep(1)
        print(Watch.lat, Watch.lon, Watch.speed)
        print(counter)


async def watch_update() -> typing.Tuple[str, float]:
    #handle: str = "0073"
    #numeric_value: float = 1.0
    handle, packet = await ble_module.rx_packet()
    numeric_value = float(packet.decode("ascii"))
    return handle, numeric_value


def watch_thread():
    global Watch
    global counter

    watch_thread_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(watch_thread_loop)

    # keys in current_data are RN4871 handles, exact values TBD
    current_data = {
        '0073': 0.0,  # lat
        '0075': 0.0,  # lon
        '0077': 0.0,  # elev
        '0079': 0.0,  # speed
        '0081': 0.0  # heart rate
    }

    while True:
        task = watch_thread_loop.create_task(watch_update())
        watch_thread_loop.run_until_complete(task)
        handle, value = task.result()
        current_data[handle] = value
        Watch = WatchData(**{handle_table[handle]: current_data[handle] for handle in current_data.keys()})
        counter += 1


if __name__ == "__main__":
    main()
