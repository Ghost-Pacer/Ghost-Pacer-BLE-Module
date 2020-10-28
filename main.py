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
        await asyncio.sleep(0)
        time.sleep(1)
        print(watch.watch_data.latitude, watch.watch_data.longitude, watch.watch_data.speed)
        print("Total packets received: " + str(watch.packets_received))


if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main())
    finally:
        main_loop.close()