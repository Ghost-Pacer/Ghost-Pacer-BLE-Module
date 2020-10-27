from collections import namedtuple
import typing
import asyncio
import time

import ble_microchip

WatchData = namedtuple('WatchData', "latitude longitude altitude speed heart_rate")

watch_data = WatchData(0.0, 0.0, 0.0, 0.0, 0.0)
packets_received = 0

_handle_table = {
    '0094': 'latitude',
    '0096': 'longitude',
    '009A': 'altitude',
    '0098': 'speed',
    '0092': 'heart_rate'
}


async def fetch_watch_data():
    global watch_data
    global packets_received

    current_data = {
        '0094': 0.0,
        '0096': 0.0,
        '009A': 0.0,
        '0098': 0.0,
        '0092': 0.0
    }

    while True:
        handle, value = await _rx_watch_data_packet()
        current_data[handle] = value
        watch_data = WatchData(**{_handle_table[handle]: current_data[handle] for handle in current_data.keys()})
        packets_received += 1


async def _rx_watch_data_packet() -> typing.Tuple[str, float]:
    handle, packet = await ble_microchip.rx_packet()
    numeric_value = float(int.from_bytes(packet, byteorder="little", signed=True))

    if _handle_table[handle] is not "heart_rate":
        numeric_value = numeric_value / 1000000

    return handle, numeric_value
