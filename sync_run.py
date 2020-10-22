from typing import List

import runup1_pb2 as run_up
import rundown1_pb2 as run_down
import RN4870 as ble_module
import google.protobuf as protobuf


async def rx_run() -> run_down.DownloadedRun:
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


async def tx_run(run: run_up.UploadedRun):
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


def serialize_run(run_data: run_up.UploadedRun) -> List[bytes]:
    # TODO
    tx_packet_size = ble_module.TX_PACKET_SIZE
    tx_sample_packet = str(tx_packet_size) + ''.join(
        ['a' for _ in range(tx_packet_size - len(str(tx_packet_size)) * 2)]) + \
                       str(tx_packet_size)
    assert len(tx_sample_packet) == tx_packet_size
    packets = [bytes.fromhex(tx_sample_packet)]
    return packets


def deserialize_run(packets: List[bytes]) -> run_down.DownloadedRun:
    # TODO
    test: str = "Test string of bytes"
    return None


if __name__ == "__main__":
    print("hello!!!!")

