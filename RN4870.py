import asyncio
import serial_asyncio
import sys

url = '/dev/ttyO4'
baudrate = 115200
rtscts = False

rx_packet_size = 100  # arbitrary limit imposed by MCP, test with 1.30 firmware?
tx_packet_size = 20  # arbitrary limit imposed by MCP

rx_handle = '0095'
tx_handle = '0092'


async def main():
    read_stream, write_stream = await serial_asyncio.open_serial_connection(url=url, baudrate=baudrate, rtscts=rtscts)
    print("serial streams created\n")
    await handshake(read_stream, write_stream)
    if sys.argv[1] == 'rx':
        packet_count = await rx_packet_count(read_stream)
        packets = []
        for i in range(packet_count):
            payload = rx_packet(read_stream)
            packets.append(payload)
        serialize_run(packets)
    else:
        assert await rx_client_is_notifiable(read_stream)
        print("subscribed")
        packets = serialize_run(None)
        packet_count = len(packets)
        await tx_packet_count(write_stream, packet_count)
        for i in range(packet_count):
            await tx_packet(write_stream, packets[i])


async def handshake(read_stream, write_stream):
    await reboot(read_stream, write_stream)
    print("waiting for connect")
    assert (await rx_message(read_stream)).startswith("CONNECT,1")
    print("\tconnected")


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
        await tx_message(write_stream, "")
        assert "Err" in await rx_message(read_stream, begin_delimiter='', end_delimiter='>')
    await tx_message(write_stream, "R,1")
    assert await rx_message(read_stream) == "REBOOT"
    await tx_message(write_stream, "$$$", end_delimiter='')
    assert await rx_message(read_stream, begin_delimiter='', end_delimiter='>') == "CMD"


async def rx_packet_count(read_stream):
    return 0


async def rx_client_is_notifiable(read_stream):
    print("tx mode")
    print("waiting for subscribe to indicate")
    return (await rx_message(read_stream)).startswith("WC")


async def rx_packet(read_stream):
    print("rx mode, awaiting data")
    res = await rx_message(read_stream)
    assert res.startswith("WV")
    payload = res.split(',')[-1]
    print("rx payload (length {}): {}".format(len(payload), rx_decode(payload)))
    return payload


def serialize_run(runData):
    tx_sample_packet = str(tx_packet_size) + ''.join(
        ['a' for _ in range(tx_packet_size - len(str(tx_packet_size)) * 2)]) + \
                       str(tx_packet_size)
    assert len(tx_sample_packet) == tx_packet_size
    packets = [tx_sample_packet]
    return packets


def deserialize_run():
    pass


async def rx_message(read_stream, begin_delimiter='%', end_delimiter='%'):
    if begin_delimiter:
        print("rx awaiting begin delimiter...")
        raw_delim = await read_stream.readuntil(begin_delimiter.encode('ascii'))
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


async def tx_packet_count(write_stream, packet_count):
    pass


async def tx_packet(write_stream, packet):
    input("Press enter to transmit")
    print("transmitting")
    encoded_packet = tx_encode(packet)
    await tx_message(write_stream, "SHW,{},{}".format(tx_handle, encoded_packet))


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
    asyncio.run(main())
