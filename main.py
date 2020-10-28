import asyncio
import time

import watch
import ble_microchip

async def main():
    await ble_microchip.open_connection()
    await ble_microchip.handshake()
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