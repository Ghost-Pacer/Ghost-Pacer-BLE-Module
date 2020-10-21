import runup1_pb2 as RunUp
import rundown1_pb2 as RunDown
import RN4870 as ble_module


async def rx_run() -> RunDown.Run:




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
    pass


async def tx_run(run: RunUp.Run) -> None:
    # Take a Protobuf run object, serialize, chunk, and send
    # First message should be the number of following messages (i.e. num chunks)
    # Then chunks should follow in order
    # Chunks should be created according to a parametric packet length (tx_packet_size)
    # Obviously individual chunks will need to be MCP encoded
    pass

def serialize_run(runData) -> List[str]:
    # TODO
    tx_sample_packet = str(tx_packet_size) + ''.join(
        ['a' for _ in range(tx_packet_size - len(str(tx_packet_size)) * 2)]) + \
                       str(tx_packet_size)
    assert len(tx_sample_packet) == tx_packet_size
    packets = [tx_sample_packet]
    return packets


def deserialize_run():
    # TODO
    pass

# # intended use
# runD = await rx_run()
#
# runU = RunUp.Run() # would be some args in there to set values
# await tx_run(runU)
