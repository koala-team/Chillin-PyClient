# -*- coding: utf-8 -*-

# python imports
import struct
import socket
import ssl
import errno

# project imports
from .config import Config


class Network:

    def __init__(self):
        self._bind = (Config.config['net']['host'], Config.config['net']['port'])
        self._sock = self._create_socket()


    def _create_socket(self):
        return ssl.wrap_socket(socket.socket())


    def connect(self):
        self._sock.settimeout(Config.config['net']['timeout'])
        self._sock.connect(self._bind)
        self._sock.settimeout(None)


    def recv_data(self):
        try:
            size = self._sock.recv(4)
            if not size:
                return b''
            size = struct.unpack('I', size)[0]
            data = b''
            while len(data) < size:
                tmp = self._sock.recv(min(1024, size - len(data)))
                if not tmp:
                    return b''
                data += tmp
            return data
        except:
            return b''


    def send_data(self, data):
        size = struct.pack('I', len(data))
        try:
            return self._sock.send(size + data)
        except socket.error as e:
            if not e.errno in [errno.EPIPE, errno.WSAECONNRESET]:
                raise e
            return -1


    def close(self):
        self._sock.close()


    def get_bind(self):
        return self._bind
