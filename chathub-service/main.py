#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：chat-meta-hub 
@File    ：main.py.py
@Email   ：2220138602@QQ.COM
@Date    ：2024/9/30 11:35 
"""
import traceback
from typing import Optional
from core import UDPServerManagerBuilder, UDPServiceManager, Client
from core import constant
from message import ChathubMessage, ChathubEventEnum, ChathubMessageEventManager

event_manager = ChathubMessageEventManager()


class ChathubServiceDispatcher:

    def __init__(self, socket_manager: Optional[UDPServiceManager] = None):
        self.socket_manager = socket_manager

    def set_socket_manager(self, socket_manager: UDPServiceManager):
        self.socket_manager = socket_manager

    @classmethod
    def on_connect_callback(cls, client: Client, data: dict):
        try:
            if event_manager.parse(data):
                event = data[event_manager.ProtocolEventKeyword]
                message = ChathubMessage(event, client, data)
                event_manager.dispatch(event, message)
        except Exception as e:
            print(f'Error: {e}')
            print(traceback.format_exc())


class ChathubServiceManager(ChathubServiceDispatcher):
    def __init__(self):
        super().__init__()

    @event_manager.register_event(ChathubEventEnum.REGISTERED)
    def on_registered(self, message: ChathubMessage):
        print(f'Client {message.client} registered')

    @event_manager.register_event(ChathubEventEnum.CONNECT)
    def on_connect(self, message: ChathubMessage):
        print(f'Client {message.client} connected')

    @event_manager.register_event(ChathubEventEnum.DISCONNECT)
    def on_disconnect(self, message: ChathubMessage):
        print(f'Client {message.client} disconnected')

    @event_manager.register_event(ChathubEventEnum.LOGIN)
    def on_login(self, message: ChathubMessage):
        print(f'Client message {message.client} login')


def main():
    chathub_service_manager = ChathubServiceManager()
    udp_socket_manager = (
        UDPServerManagerBuilder('127.0.0.1', 8888)
        .register(chathub_service_manager.on_connect_callback)
        .build()
    )
    chathub_service_manager.set_socket_manager(udp_socket_manager)
    udp_socket_manager.start()
    print(f"* ************************************************************************* *")
    print(f"* Link: {constant.uri(udp_socket_manager.host, udp_socket_manager.port)}")
    print(f"* Service started, waiting for connections...")
    print(f"* ************************************************************************* *")
    udp_socket_manager.join()


if __name__ == '__main__':
    main()
