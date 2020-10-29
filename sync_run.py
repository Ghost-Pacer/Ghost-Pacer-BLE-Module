"""Upload/download run data to and from the Ghost Pacer iOS app

Download a run from the Ghost Pacer iOS app as a DownloadedRun protobuf object, or upload a UploadedRun protobuf
object to the app. You can only use this module if you've already opened a connection to a device with the
ble_microchip module.

    Typical usage example:
    downloaded_run = await download_run()
    ...
    run_to_upload = UploadedRun(...)
    await upload_run(run_to_upload)
"""

from typing import List

from runup1_pb2 import UploadedRun
from rundown1_pb2 import DownloadedRun
import ble_microchip
import asyncio
import math


# ***** DOWNLOAD/UPLOAD RUN *****
async def download_run() -> DownloadedRun:
    if not ble_microchip.is_connected():
        print("Error: Tried reading without active connection")
        return

    packet_count = await ble_microchip.rx_packet_count()
    print("Packet count: " + str(packet_count))
    packets = []
    for i in range(packet_count):
        print("Packets received: " + str(i + 1) + "/" + str(packet_count))
        _, received_packet = await ble_microchip.rx_packet()
        packets.append(received_packet)
    return _deserialize_run(packets)


async def upload_run(run: UploadedRun):
    if not ble_microchip.is_connected():
        print("Error: Tried writing without active connection")
        return

    assert await ble_microchip.device_is_notifiable()
    packets = _serialize_run(run)
    packet_count = len(packets)
    await ble_microchip.tx_packet_count(packet_count)
    for i in range(packet_count):
        await asyncio.sleep(0.05)
        await ble_microchip.tx_packet(packets[i])


# ***** SERIALIZE/DESERIALIZE RUN *****
def _serialize_run(run: UploadedRun) -> List[bytes]:
    run_data = run.SerializeToString()
    run_data_size = len(run_data)

    tx_packet_size = ble_microchip.TX_PACKET_SIZE
    chunked_run_data = []
    for i in range(math.ceil(run_data_size / tx_packet_size)):
        start_index = i * tx_packet_size
        end_index = start_index + tx_packet_size + 1
        chunk = run_data[start_index:end_index]
        chunked_run_data.append(chunk)
    return chunked_run_data


def _deserialize_run(packets: List[bytes]) -> DownloadedRun:
    combined_packet = bytearray()
    for i in range(len(packets)):
        combined_packet.extend(packets[i])
    parsed_run = DownloadedRun()
    parsed_run.ParseFromString(combined_packet)
    return parsed_run
