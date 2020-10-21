import runup1_pb2 as RunUp
import rundown1_pb2 as RunDown
import RN4870 as BLEModule

from collections import namedtuple
import typing
import threading
import time

#### APP STUFF ####
rx_packet_size = 100 # arbitrary limit imposed by MCP, test with 1.30 firmware?
tx_packet_size = 20 # arbitrary limit imposed by MCP

rx_handle = '0095'
tx_handle = '0092'

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

# intended use
runD = await rx_run()

runU = RunUp.Run() # would be some args in there to set values
await tx_run(runU)


#### WATCH STUFF ####
# the more i look at this it would be easier in some sense with protobuf because the messages would be atomic
# however a piecewise delivery is the most likely way it'll happen when we implement backing layers
# for more smartwatches so we might as well deal with it, this makes watch side stuff easier definitely

async def watch_update() -> typing.Tuple[str, float]:
    # Process a single characteristic change (WV message) and return up its handle and value
    pass

handle_table = {
        '0073': 'lat',
        '0075': 'lon',
        '0077': 'elev',
        '0079': 'speed',
        '0081': 'heart_rate'
}

WatchData = namedtuple('WatchData', "lat lon elev speed heart_rate")
# PyCharm (and maybe other IDEs?) doesn't properly handle a namedtuple constructed from potentially dynamic data
# to fix syntax highlighting replace handle_table.values() with "lat lon elev speed heart_rate"

Watch: WatchData = WatchData(0.0, 0.0, 0.0, 0.0, 0.0)
# global variable to make access similar to threaded AGPS3 implemetation

def watch_thread():
    global Watch

    # keys in current_data are RN4871 handles, exact values TBD
    current_data = {
        '0073': 0.0, # lat
        '0075': 0.0, # lon
        '0077': 0.0, # elev
        '0079': 0.0, # speed
        '0081': 0.0  # heart rate
    }

    while True:
        handle, value = await watch_update()
        current_data[handle] = value
        Watch = WatchData(**{handle_table[handle]: current_data[handle] for handle in current_data.keys()})

# intended use

threading.Thread(target=watch_thread).start()
while True:
    time.sleep(1)
    print(Watch.lat, Watch.lon, Watch.speed)


