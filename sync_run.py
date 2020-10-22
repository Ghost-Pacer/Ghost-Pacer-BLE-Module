from typing import List

import runup1_pb2 as RunUp
import rundown1_pb2 as RunDown
import RN4870 as ble_module


async def rx_run() -> RunDown.Run:
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


async def tx_run(run: RunUp.Run) -> None:
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


def serialize_run(runData: RunUp.Run) -> List[bytes]:
    # TODO
    tx_packet_size = ble_module.TX_PACKET_SIZE
    tx_sample_packet = str(tx_packet_size) + ''.join(
        ['a' for _ in range(tx_packet_size - len(str(tx_packet_size)) * 2)]) + \
                       str(tx_packet_size)
    assert len(tx_sample_packet) == tx_packet_size
    packets = [bytes.fromhex(tx_sample_packet)]
    return packets


def deserialize_run(packets: List[bytes]) -> RunDown.Run:
    # TODO
    return RunDown.Run()
