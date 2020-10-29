"""Receive GPS and heart rate data from Apple Watch.

The watch_data global variable holds the most recent data fetched from the apple watch. This module should be used
with asyncio to receive data asynchronously. This module depends on the ble_microchip module, and assumes the client
has already connected to the Apple Watch.

    Typical usage example:

    main_loop = asyncio.get_event_loop()
    main_loop.create_task(fetch_watch_data())

    while ...:
        ... do unrelated tasks ...
        await asyncio.sleep(0) # This is needed in busy waiting loops to process tasks in the event loop
        latitude = watch.latitude
        longitude = watch.longitude
        ... do stuff with watch data ...
"""

from collections import namedtuple

import ble_microchip

WatchData = namedtuple("WatchData", "latitude longitude altitude speed heart_rate")

watch_data = WatchData(0.0, 0.0, 0.0, 0.0, 0.0)
packets_received = 0

_handle_table = {
    "0094": "latitude",
    "0096": "longitude",
    "009A": "altitude",
    "0098": "speed",
    "0092": "heart_rate",
}


async def fetch_watch_data():
    global watch_data
    global packets_received

    current_data = {"0094": 0.0, "0096": 0.0, "009A": 0.0, "0098": 0.0, "0092": 0.0}

    while True:
        handle, value = await _rx_watch_data_packet()
        if not handle:
            continue

        current_data[handle] = value
        watch_data = WatchData(
            **{
                _handle_table[handle]: current_data[handle]
                for handle in current_data.keys()
            }
        )
        packets_received += 1


async def _rx_watch_data_packet() -> (str, float):
    handle, packet = await ble_microchip.rx_packet()
    numeric_value = float(int.from_bytes(packet, byteorder="little", signed=True))

    if handle in _handle_table:
        data_type = _handle_table[handle]
        if data_type is not "heart_rate":
            numeric_value = numeric_value / 1000000
    else:
        return "", 0

    return handle, numeric_value
