#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：chathub-IM
@File    ：core.py
@Email   ：2220138602@QQ.COM
@Date    ：2024/9/18 15:00 
"""
import dataclasses
import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional, Callable


class UDPSocket:
    def __init__(self, host: str, port: int, buffer_size: int = 1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def send(self, data: bytes, addr: Tuple[str, int]) -> None:
        self.socket.sendto(data, addr)

    def receive(self, buffer_size: int = None) -> Tuple[bytes, Tuple[str, int]]:
        buffer_size = buffer_size or self.buffer_size
        return self.socket.recvfrom(buffer_size)

    def close(self) -> None:
        self.socket.close()


@dataclasses.dataclass
class Client:
    host: str
    port: int
    addr: Tuple[str, int]
    socket: UDPSocket
    service_manager: 'UDPServiceManager'

    def sendto(self, data: dict) -> None:
        self.service_manager.sendto(data, self.addr)


class UDPServiceManager(threading.Thread):
    def __init__(self, udp_socket: UDPSocket, on_receive_callback: Callable[[Client, dict], None]):
        super().__init__()
        self.udp_socket = udp_socket
        self._stop_event = threading.Event()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.on_receive_callback: Optional[Callable[[Client, dict], None]] = on_receive_callback

    @property
    def host(self):
        return self.udp_socket.host

    @property
    def port(self):
        return self.udp_socket.port

    def __on_socket_receive(self, data: bytes, addr: Tuple[str, int]) -> None:
        try:
            data = data.decode('utf-8')
            data = eval(data)
        except Exception as e:
            print(f"Error decoding data: {e}")
            return
        client = Client(host=addr[0], port=addr[1], addr=addr, socket=self.udp_socket, service_manager=self)
        print(">>", data),
        self.on_receive_callback(client, data)

    def run(self) -> None:
        while not self._stop_event.is_set():
            data, addr = self.udp_socket.receive()
            self.executor.submit(self.__on_socket_receive, data, addr)

    def sendto(self, data: dict, addr: Tuple[str, int]) -> None:
        data_str = json.dumps(data)
        self.udp_socket.send(data_str.encode('utf-8'), addr)

    def stop(self) -> None:
        self._stop_event.set()
        self.executor.shutdown(wait=True)
        self.udp_socket.close()
        print("Server stopped.")


class UDPServerManagerBuilder:
    def __init__(self, host: str, port: int):
        self.__config = {
            "udp_socket": UDPSocket(host, port)
        }

    def register(self, func):
        self.__config["on_receive_callback"] = func
        return self

    def build(self) -> UDPServiceManager:
        return UDPServiceManager(**self.__config)


