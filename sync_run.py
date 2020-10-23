from typing import List

from runup1_pb2 import UploadedRun
from rundown1_pb2 import DownloadedRun
import RN4870 as ble_module
import math


async def rx_run() -> DownloadedRun:
    if not ble_module.is_connected():
        print("ERROR: Tried reading without active connection")
        return

    await ble_module.flush_read_stream()
    packet_count = await ble_module.rx_packet_count()
    packets: List[bytes] = []
    for i in range(packet_count):
        _, received_packet = await ble_module.rx_packet()
        packets.append(received_packet)
    return deserialize_run(packets)


async def tx_run(run: UploadedRun):
    if not ble_module.is_connected():
        print("ERROR: Tried writing without active connection")
        return

    await ble_module.flush_write_stream()
    assert await ble_module.rx_client_is_notifiable()
    packets = serialize_run(run)
    packet_count = len(packets)
    await ble_module.tx_packet_count(packet_count)
    for i in range(packet_count):
        await ble_module.tx_packet(packets[i])


def serialize_run(run: UploadedRun) -> List[bytes]:
    run_data: bytearray = run.SerializeToString()
    run_data_size = len(run_data)
    print(run_data)
    print(run_data[0].to_bytes(1, "little"))

    tx_packet_size = ble_module.TX_PACKET_SIZE
    chunked_run_data: List[bytes] = []
    for i in range(math.ceil(run_data_size / tx_packet_size)):
        chunk: bytearray = bytearray()
        for j in range(tx_packet_size):
            index = i * j + j
            if index >= run_data_size:
                break
            chunk.extend(run_data[index].to_bytes(1, "little"))
        chunked_run_data.append(bytes(chunk))
    return chunked_run_data


def deserialize_run(packets: List[bytes]) -> DownloadedRun:
    combined_packet: bytearray = bytearray()
    for i in range(len(packets)):
        combined_packet.extend(packets[i])
    parsed_run: DownloadedRun = DownloadedRun()
    parsed_run.ParseFromString(combined_packet)
    return parsed_run
