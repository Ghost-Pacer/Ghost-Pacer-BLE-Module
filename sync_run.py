from typing import List

import runup1_pb2 as RunUp
import rundown1_pb2 as RunDown
import RN4870 as ble_module


async def rx_run() -> RunDown.Run:
    transfer_type = ble_module.TransferType.READ
    await ble_module.open_connection(transfer_type)
    packet_count = await ble_module.rx_packet_count()
    packets: List[bytes] = []
    for i in range(packet_count):
        received_packet = await ble_module.rx_packet()
        packets.append(received_packet)
    return deserialize_run(packets)

    # Await a complete run being sent
    # First flush the receive queue
    # Assume the first packet will be an int that is the number of packets to follow
    # Collect each of the following packets as they arrive
    # by converting ASCII-encoded hex to a BLOB representation (python bytes or similar)
    # After all packets have arrived, combine the BLOB representations into one BLOB and deserialize
    # using Protobuf, and return the Protobuf object.
    # *** I think Protobuf operates on bytes rather than str in python but there may be a bit of experimental
    # *** stuff to work out here as far as getting the stupid Microchip encoding stripped away and into the
    # *** format that Protobuf expects the data for deserializing.
    # *** might be worth a bit of googling or just wait and test
    # *** or ig maybe make a unit test with simulated MCP encoded data if ahead of schedule


async def tx_run(run: RunUp.Run) -> None:
    transfer_type = ble_module.TransferType.WRITE
    await ble_module.open_connection(transfer_type)
    packets = serialize_run(run)
    packet_count = len(packets)
    await ble_module.tx_packet_count(packet_count)
    for i in range(packet_count):
        await ble_module.tx_packet(packets[i])

    # Take a Protobuf run object, serialize, chunk, and send
    # First message should be the number of following messages (i.e. num chunks)
    # Then chunks should follow in order
    # Chunks should be created according to a parametric packet length (tx_packet_size)
    # Obviously individual chunks will need to be MCP encoded


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