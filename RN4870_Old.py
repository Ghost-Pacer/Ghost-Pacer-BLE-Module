import asyncio
import serial_asyncio
import sys

url = '/dev/ttyS1'
baudrate = 115200
rtscts = False

rx_packet_size = 100 # arbitrary limit imposed by MCP, test with 1.30 firmware?
tx_packet_size = 20 # arbitrary limit imposed by MCP
tx_sample_packet = str(tx_packet_size) + ''.join(['a' for _ in range(tx_packet_size - len(str(tx_packet_size)) * 2)]) + \
                   str(tx_packet_size) # '100aaa...aaa100' with len(sample_packet) = 100
assert len(tx_sample_packet) == tx_packet_size

rx_handle = '0095'
tx_handle = '0092'


async def main():
    read_stream, write_stream = await serial_asyncio.open_serial_connection(url=url, baudrate=baudrate, rtscts=rtscts)
    print("serial streams created\n")
    '''
    REBOOT SEQUENCE
    await tx_message(write_stream, "$$$", end_delimiter='')
    assert await rx_message(read_stream, begin_delimiter='', end_delimiter='>') == "CMD"
    await tx_message(write_stream, "R,1")
    assert await rx_message(read_stream) == "REBOOT"
    '''
    await reboot(read_stream, write_stream)
    print("waiting for connect")
    assert (await rx_message(read_stream)).startswith("CONNECT,1")
    print("\tconnected")

    if (sys.argv[1] == 'rx'):
        while True:
            print("rx mode, awaiting data")
            res = await rx_message(read_stream)
            assert res.startswith("WV")
            payload = res.split(',')[-1]
            print("rx payload (length {}): {}".format(len(payload), rx_decode(payload)))
    else:
        print("tx mode")
        print("waiting for subscribe to indicate")
        assert (await rx_message(read_stream)).startswith("WC")
        print("subscribed")
        while True:
            input("Press enter to transmit")
            print("transmitting")
            await tx_message(write_stream, "SHW,{},{}".format(tx_handle, tx_encode(tx_sample_packet)))



async def reboot(read_stream, write_stream):
    # assume not in command mode
    print("rebooting")
    await tx_message(write_stream, "$$$", end_delimiter='')
    try:
        # wait up to 1 sec for CMD>
        res = await asyncio.wait_for(rx_message(read_stream, begin_delimiter='', end_delimiter='>'), timeout=1.0)
    except asyncio.TimeoutError:
        # nothing back, so already in command mode
        # send newline to clear, will error out
        await asyncio.sleep(0)
        await tx_message(write_stream, "")
        assert "Err" in await rx_message(read_stream, begin_delimiter='', end_delimiter='>')
    await tx_message(write_stream, "R,1")
    assert await rx_message(read_stream) == "REBOOT"
    await tx_message(write_stream, "$$$", end_delimiter='')
    assert await rx_message(read_stream, begin_delimiter='', end_delimiter='>') == "CMD"


async def rx_message(read_stream, begin_delimiter='%', end_delimiter='%'):
    if begin_delimiter:
        print("rx awaiting begin delimiter...")
        raw_delim = await read_stream.readuntil(begin_delimiter.encode('ascii'))

        # print("\t{}".format(raw_delim))
        # assert raw_delim.decode('ascii') == begin_delimiter

        print("\trx consumed: {}".format(repr(raw_delim.decode('ascii'))))

    print("rx awaiting content...")

    raw_message = await read_stream.readuntil(end_delimiter.encode('ascii'))
    # convert bytestream to console text/utf-8 and strip trailing '%'
    message = raw_message.decode('ascii')[:-len(end_delimiter)]

    print("\trx consumed: {}".format(repr(raw_message.decode('ascii'))))

    return message

def rx_decode(message):
    # unpack string of ASCII-encoded hex which itself encodes ASCII
    return bytes.fromhex(message).decode('ascii')


async def tx_message(write_stream, message, end_delimiter='\n'):
    complete_message = message
    if end_delimiter is not None:
        complete_message += end_delimiter
    write_stream.write(complete_message.encode('ascii'))

    print("tx draining...")

    await write_stream.drain()

    print("\ttx drained: <{}>".format(repr(message + end_delimiter)))
    # repr -> replace special characters with escape sequences

def tx_encode(payload):
    # pack string to ASCII-encoded hex string
    return payload.encode('ascii').hex()

if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    try:
        main_loop.run_until_complete(main())
    finally:
        main_loop.close()
