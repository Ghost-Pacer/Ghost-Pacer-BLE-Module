import asyncio

import watch
import sync_run
import ble_microchip
from rundown1_pb2 import DownloadedRun
from runup1_pb2 import UploadedRun


async def main():
    await phone_upload_test()


async def phone_download_test():
    await ble_microchip.open_connection()
    await ble_microchip.connect_to_device()
    print("Began fetching phone data...")
    run = await sync_run.rx_run()
    print(run)


async def phone_upload_test():
    await ble_microchip.open_connection()
    await ble_microchip.connect_to_device()

    file = open("./downloaded_run.txt", "rb")
    serialized_run = file.read()
    file.close()

    run = DownloadedRun()
    run.ParseFromString(serialized_run)

    await sync_run.tx_run(run)
    print("Finished transmitting data.")


async def watch_test():
    await ble_microchip.open_connection()
    await ble_microchip.connect_to_device()
    print("Began fetching watch data...")

    main_loop = asyncio.get_event_loop()
    main_loop.create_task(watch.fetch_watch_data())

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


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main())
    finally:
        main_loop.close()
