import asyncio
import serial_asyncio
import sys
from enum import Enum

StreamReader = asyncio.StreamReader
StreamWriter = asyncio.StreamWriter

URL = '/dev/ttyO4'
BAUDRATE = 115200
RTSCTS = False

RX_PACKET_SIZE = 100  # arbitrary limit imposed by MCP, test with 1.30 firmware?
TX_PACKET_SIZE = 20  # arbitrary limit imposed by MCP

RX_HANDLE = '0095'
TX_HANDLE = '0092'

read_stream: StreamReader
write_stream: StreamWriter


class TransferType(Enum):
    READ = 0
    WRITE = 1


# ***** ESTABLISH CONNECTION *****

async def open_connection(transfer_type: TransferType):
    global read_stream, write_stream
    read_stream, write_stream = await serial_asyncio.open_serial_connection(url=URL, baudrate=BAUDRATE, rtscts=RTSCTS)
    print("serial streams created\n")
    assert await _handshake()
    print("\tconnected")
    _flush_stream(transfer_type)
    if TransferType.WRITE:
        assert await _rx_client_is_notifiable()


def _flush_stream(stream_type: TransferType):
    # TODO
    pass


async def _handshake() -> bool:
    await _reboot()
    print("waiting for connect")
    return (await _rx_message()).startswith("CONNECT,1")


async def _reboot():
    # assume not in command mode
    print("rebooting")
    await _tx_message("$$$", end_delimiter='')
    try:
        # wait up to 1 sec for CMD>
        res = await asyncio.wait_for(_rx_message(begin_delimiter='', end_delimiter='>'), timeout=1.0)
    except asyncio.TimeoutError:
        # nothing back, so already in command mode
        # send newline to clear, will error out
        await _tx_message("")
        assert "Err" in await _rx_message(begin_delimiter='', end_delimiter='>')
    await _tx_message("R,1")
    assert await _rx_message() == "REBOOT"
    await _tx_message("$$$", end_delimiter='')
    assert await _rx_message(begin_delimiter='', end_delimiter='>') == "CMD"


# ***** RECEIVE DATA *****

async def rx_packet_count() -> int:
    # Assumes this is called before starting to receive all packets
    return int(await rx_packet())


async def _rx_client_is_notifiable() -> bool:
    # Assumes already in transmit mode
    print("tx mode")
    print("waiting for subscribe to indicate")
    return (await _rx_message()).startswith("WC")


async def rx_packet() -> str:
    print("rx mode, awaiting data")
    res = await _rx_message()
    assert res.startswith("WV")
    payload = res.split(',')[-1]
    decoded_payload = _rx_decode(payload)
    print("rx payload (length {}): {}".format(len(payload), decoded_payload))
    return decoded_payload


async def _rx_message(begin_delimiter: str = '%', end_delimiter: str = '%') -> str:
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


def _rx_decode(message: str) -> str:
    # unpack string of ASCII-encoded hex which itself encodes ASCII
    return bytes.fromhex(message).decode('ascii')


# ***** TRANSMIT DATA *****

async def tx_packet_count(packet_count: int):
    await tx_packet(str(packet_count))


async def tx_packet(packet: str):
    input("Press enter to transmit")
    print("transmitting")
    encoded_packet = _tx_encode(packet)
    await _tx_message("SHW,{},{}".format(TX_HANDLE, encoded_packet))


async def _tx_message(message: str, end_delimiter: str = '\n'):
    complete_message = message
    if end_delimiter is not None:
        complete_message += end_delimiter
    write_stream.write(complete_message.encode('ascii'))
    print("tx draining...")
    await write_stream.drain()
    print("\ttx drained: <{}>".format(repr(message + end_delimiter)))
    # repr -> replace special characters with escape sequences


def _tx_encode(payload: str) -> str:
    # pack string to ASCII-encoded hex string
    return payload.encode('ascii').hex()
