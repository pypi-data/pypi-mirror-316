import socket
import asyncio
import struct
import json
from asyncio import StreamReader, StreamWriter

from roc.channel_manager import ChannelManager
from roc.data_formatter import DataFormatter
from roc.id_generator import IdGenerator
from roc.packer import Packer
from roc.packet import Packet
from roc.request import Request
from roc.request import Response
from roc.request import make_response
from roc.packet import PING


class SocketException(Exception):
    def __init__(self, message, error_code: int = 0):
        super().__init__(message)
        self.error_code = error_code


class RequestException(Exception):
    def __init__(self, message, error_code: int = 0):
        super().__init__(message)
        self.error_code = error_code


class Client:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.reader: StreamReader | None = None
        self.writer: StreamWriter | None = None
        self.packer: Packer = Packer()
        self.channelManager: ChannelManager = ChannelManager()
        self.idGenerator: IdGenerator = IdGenerator()
        self.dataFormatter: DataFormatter = DataFormatter()

        asyncio.create_task(self.loop())
        asyncio.create_task(self.heartbeat())

    async def loop(self):
        while True:
            if self.writer is None:
                await asyncio.sleep(1)
                continue

            try:
                prefix = await self.recv(4)
                length = struct.unpack(">I", prefix)[0]
                body = await self.recv(length)

                packet = self.packer.unpack(prefix + body)
                if packet.is_heartbeat():
                    continue

                chan = self.channelManager.get(packet.id)
                if chan is not None:
                    await chan.push(packet.body)

            except SocketException:
                self.writer = None
                self.reader = None
                continue
            except Exception as exception:
                print(f"loop发生了异常: {exception}")
                await asyncio.sleep(1)
                continue

    async def heartbeat(self):
        while True:
            if self.writer is None:
                await asyncio.sleep(1)
                continue

            try:
                await asyncio.sleep(10)

                await self.send(Packet(0, PING))
            except SocketException:
                self.writer = None
                self.reader = None
                continue
            except Exception as exception:
                print(f"心跳发生了异常: {exception}")
                await asyncio.sleep(1)
                continue

    async def recv(self, length: int) -> bytes:
        result: bytes = b''
        while True:
            res = await self.reader.read(length - len(result))
            if len(res) == 0:
                raise SocketException("read failed")
            result += res
            if len(result) >= length:
                return result

    async def send(self, packet: Packet) -> bool:
        if self.writer is None:
            await self.start()

        self.writer.write(self.packer.pack(packet))
        return True

    async def request(self, request: Request) -> Response:
        key = self.idGenerator.generate()
        body = self.dataFormatter.format_request(request)
        packet = Packet(key, body)
        chan = self.channelManager.get(key, True)

        try:
            await self.send(packet)

            res = await chan.pop()
            if res is False:
                raise RequestException("request failed")

            data = json.loads(res)

            return make_response(data)
        except SocketException:
            self.reader = None
            self.writer = None
        finally:
            self.channelManager.close(key)

    async def start(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self.reader = reader
        self.writer = writer
