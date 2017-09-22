# -*- coding: utf-8 -*-

# project imports
from .config import Config
from .helpers.parser import Parser


class Protocol:

    def __init__(self, network):
        self._network = network
        self._parser = Parser(Config.config['general']['command_files'])


    def recv_msg(self):
        data = self._network.recv_data()
        if not data:
            return None
        msg_type, msg, _, _ = self._parser.decode(data)
        return msg_type, msg


    def send_msg(self, msg):
        data = self._parser.encode(msg)
        self._network.send_data(data)
