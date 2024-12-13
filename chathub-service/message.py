#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：chat-meta-hub 
@File    ：message.py
@Email   ：2220138602@QQ.COM
@Date    ：2024/9/29 9:58 
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable
from core import Client


@dataclass
class ChathubMessage:
    event: str
    client: Client
    data: dict


class ChathubEventEnum(Enum):
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTERED = "registered"
    MESSAGE = 'message'
    ERROR = 'error'
    HEARTBEAT = 'heartbeat'
    UNKNOWN = 'unknown'


class ChathubMessageEventManager(object):   #
    ProtocolEventKeyword = 'event'
    ProtocolEventValue = 'value'
    __event_callback_table = {}

    @classmethod
    def parse(cls, data: dict) -> bool:
        return cls.ProtocolEventKeyword in data.keys()

    @classmethod
    def register_event(cls, event: ChathubEventEnum):
        def wrapper(func: Callable[[ChathubMessage], None]):
            cls.__event_callback_table[event] = func
            return func
        return wrapper

    @classmethod
    def dispatch(cls, event: str, data: ChathubMessage):
        if event in cls.__event_callback_table.keys():
            cls.__event_callback_table[event](data)
        else:
            print(f'Event {event} not found')



