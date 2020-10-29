import asyncio
import serial_asyncio

StreamReader = asyncio.StreamReader
StreamWriter = asyncio.StreamWriter

_URL = '/dev/ttyS1'
_BAUDRATE = 115200
_RTSCTS = False

TX_PACKET_SIZE = 20  # arbitrary limit imposed by MCP
_TX_HANDLE = '0072'

_DEBUG = False

_read_stream = None
_write_stream = None


# ***** ESTABLISH CONNECTION *****
async def open_connection():
    global _read_stream, _write_stream
    _read_stream, _write_stream = await serial_asyncio.open_serial_connection(url=_URL, baudrate=_BAUDRATE, rtscts=_RTSCTS)
    if _DEBUG: print("serial streams created\n")


def is_connected() -> bool:
    return False if _read_stream is None else True


async def handshake() -> bool:
    await _reboot()
    print("Waiting for connect...")
    return (await _rx_message()).startswith("CONNECT,1")


async def _reboot():
    # assume not in command mode
    if _DEBUG: print("rebooting")
    await _tx_message("$$$", end_delimiter='')
    try:
        # wait up to 1 sec for CMD>
        res = await asyncio.wait_for(_rx_message(begin_delimiter='', end_delimiter='>'), timeout=1.0)
    except asyncio.TimeoutError:
        # nothing back, so already in command mode
        # send newline to clear, will error out
        await asyncio.sleep(0)
        await _tx_message("")
        assert "Err" in await _rx_message(begin_delimiter='', end_delimiter='>')
    await _tx_message("R,1")
    assert await _rx_message() == "REBOOT"
    await _tx_message("$$$", end_delimiter='')
    assert await _rx_message(begin_delimiter='', end_delimiter='>') == "CMD"


async def close_connection():
    _write_stream.close()
    await _write_stream.wait_closed()


# ***** RECEIVE DATA *****
async def flush_read_stream():
    _read_stream.feed_eof()
    await _read_stream.read()


async def rx_packet_count() -> int:
    # Assumes this is called before starting to receive all packets
    _, payload = await rx_packet()
    return int.from_bytes(payload, byteorder="little", signed=True)


async def rx_client_is_notifiable() -> bool:
    # Assumes already in transmit mode
    if _DEBUG: print("tx mode")
    if _DEBUG: print("waiting for subscribe to indicate")
    return (await _rx_message()).startswith("WC")


async def rx_packet() -> (str, bytes):
    if _DEBUG: print("rx mode, awaiting data")
    res = await _rx_message()
    if not res.startswith("WV"): return ("", int(0).to_bytes(1, "little"))

    handle = res.split(',')[1]
    payload = res.split(',')[-1]
    decoded_payload = _rx_decode(payload)
    if _DEBUG: print("rx payload (length {}): {}".format(len(payload), decoded_payload))
    return handle, decoded_payload


async def _rx_message(begin_delimiter: str = '%', end_delimiter: str = '%') -> str:
    if begin_delimiter:
        if _DEBUG: print("rx awaiting begin delimiter...")
        raw_delim = await _read_stream.readuntil(begin_delimiter.encode('ascii'))
        if _DEBUG: print("\trx consumed: {}".format(repr(raw_delim.decode('ascii'))))
    if _DEBUG: print("rx awaiting content...")
    raw_message = await _read_stream.readuntil(end_delimiter.encode('ascii'))
    # convert bytestream to console text/utf-8 and strip trailing '%'
    message = raw_message.decode('ascii')[:-len(end_delimiter)]
    if _DEBUG: print("\trx consumed: {}".format(repr(raw_message.decode('ascii'))))
    return message


def _rx_decode(message: str) -> bytes:
    return bytes.fromhex(message)


# ***** TRANSMIT DATA *****
async def flush_write_stream():
    await _write_stream.drain()


async def tx_packet_count(packet_count: int):
    packet_count_bytes = packet_count.to_bytes((packet_count.bit_length() // 8) + 1, "little")
    await tx_packet(packet_count_bytes)


async def tx_packet(packet: bytes):
    if _DEBUG: print("transmitting")
    encoded_packet = _tx_encode(packet)
    await _tx_message("SHW,{},{}".format(_TX_HANDLE, encoded_packet))


async def _tx_message(message: str, end_delimiter: str = '\n'):
    complete_message = message
    if end_delimiter is not None:
        complete_message += end_delimiter
    _write_stream.write(complete_message.encode('ascii'))
    if _DEBUG: print("tx draining...")
    await flush_write_stream()
    if _DEBUG: print("\ttx drained: <{}>".format(repr(message + end_delimiter)))
    # repr -> replace special characters with escape sequences


def _tx_encode(payload: bytes) -> str:
    return payload.hex()
