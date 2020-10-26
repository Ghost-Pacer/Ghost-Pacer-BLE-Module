from collections import namedtuple
import typing
import threading
import asyncio
import time

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
counter = 1


async def main():
    await ble_module.open_connection()
    print("hi")
    threading.Thread(target=watch_thread).start()

    global counter
    while True:
        time.sleep(1)
        print(Watch.lat, Watch.lon, Watch.speed)
        print(counter)


async def watch_update() -> typing.Tuple[str, float]:
    handle = "0094"
    numeric_value = 1.0
    #handle, packet = await ble_module.rx_packet()
    #numeric_value = float(packet.decode("ascii"))
    await asyncio.sleep(1)
    return handle, numeric_value


def watch_thread():
    global Watch
    global counter

    watch_thread_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(watch_thread_loop)

    # keys in current_data are RN4871 handles, exact values TBD
    current_data = {
        '0094': 0.0,
        '0096': 0.0,
        '009A': 0.0,
        '0098': 0.0,
        '0092': 0.0
    }

    while True:
        task = watch_thread_loop.create_task(watch_update())
        watch_thread_loop.run_until_complete(task)
        handle, value = task.result()
        current_data[handle] = value
        Watch = WatchData(**{handle_table[handle]: current_data[handle] for handle in current_data.keys()})
        counter += 1


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main())
    finally:
        main_loop.close()
