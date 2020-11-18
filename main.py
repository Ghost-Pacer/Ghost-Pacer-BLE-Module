import asyncio
import time

import watch
import sync_run
import ble_microchip
from rundown1_pb2 import DownloadedRun
from runup1_pb2 import UploadedRun


async def main():
    # await upload_to_phone_test("./test_runs/uploaded_run.txt")
    # await download_from_phone_test()
    await watch_test()


async def download_from_phone_test():
    await ble_microchip.open_connection()
    await ble_microchip.flush_read_stream()
    await ble_microchip.connect_device()
    print("Began fetching phone data...")
    run = await sync_run.download_run()
    print(run)
    assert await ble_microchip.disconnect_device()


async def upload_to_phone_test(file_path: str):
    file = open(file_path, "rb")
    serialized_run = file.read()
    file.close()

    run = UploadedRun()
    run.ParseFromString(serialized_run)

    await ble_microchip.open_connection()
    assert await ble_microchip.connect_device()
    await sync_run.upload_run(run)
    assert await ble_microchip.disconnect_device()
    print("Finished transmitting data.")


async def watch_test():
    await ble_microchip.open_connection()
    assert await ble_microchip.connect_device()
    print("Began fetching watch data...")

    main_loop = asyncio.get_event_loop()
    fetch_watch_data_task = main_loop.create_task(watch.fetch_watch_data())

    try:
        while True:
            await asyncio.sleep(1)
            watch_data = watch.watch_data
            print("Latitude: " + str(watch_data.latitude))
            print("Longitude: " + str(watch_data.longitude))
            print("Altitude: " + str(watch_data.altitude))
            print("Speed: " + str(watch_data.speed))
            print("Heart Rate: " + str(watch_data.heart_rate))
            print("Total packets received: " + str(watch.packets_received))
            print("**********")
            print()
    except:
        # print("Cleaning up...")
        # fetch_watch_data_task.cancel()

        packet_latencies_total = 0
        packet_latencies_count = len(watch.packet_latencies)
        for i in range(packet_latencies_count):
            packet_latencies_total += watch.packet_latencies[i]

        average_packet_latency = packet_latencies_total / packet_latencies_count

        print("\n\n")
        print("Packet Latencies: " + str(watch.packet_latencies))
        print("\n\n")
        print("Average Packet Latency: " + str(average_packet_latency))
        print("\n\n")


async def export_protobuf(file_path: str):
    total_distance = 0
    start_time = 0
    start_lat = 0
    start_lon = 0
    track_start_point = 0
    comp_lat_dist = []
    comp_lat = []
    comp_lon_dist = []
    comp_lon = []
    saved_time = []

    run_data = UploadedRun()
    run_data.totalDistance = total_distance
    run_data.startTime = start_time
    run_data.startLat = start_lat
    run_data.startLon = start_lon
    run_data.trackStartPoint = track_start_point
    run_data.compLatDist.extend(comp_lat_dist)
    run_data.compLat.extend(comp_lat)
    run_data.compLonDist.extend(comp_lon_dist)
    run_data.compLon.extend(comp_lon)
    run_data.savedTime.extend(saved_time)

    print(run_data)

    file = open(file_path, "wb")
    file.write(run_data.SerializeToString())
    file.close()


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(watch_test())
    finally:
        main_loop.close()
