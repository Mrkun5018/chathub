#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：chat-meta-hub 
@File    ：constant.py
@Email   ：2220138602@QQ.COM
@Date    ：2024/9/29 13:40 
"""

HTTP = "http"
HTTPS = "https"
URI_FORMAT = "{protocol}://{host}:{port}/"


def uri(host: str, port: int, protocol: str = HTTP) -> str:
    return URI_FORMAT.format(protocol=protocol, host=host, port=port)