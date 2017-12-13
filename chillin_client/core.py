# -*- coding: utf-8 -*-

# python imports
import sys

from time import sleep
from threading import Thread

if sys.version_info > (3,):
    from queue import Queue
else:
    from Queue import Queue

# project imports
from .config import Config
from .network import Network
from .protocol import Protocol
from .helpers.messages import JoinOfflineGame, JoinOnlineGame, ClientJoined, \
        StartGame, EndGame, BaseSnapshot, RealtimeSnapshot, TurnbasedSnapshot
from .helpers.datetime import utcnowts
from .helpers.logger import log


class Core:

    def __init__(self):
        self._game_running = False
        self._command_send_queue = Queue()

        self._network = Network()
        self._protocol = Protocol(self._network)


    def register_ai(self, ai):
        ai.set_command_send_queue(self._command_send_queue)
        self._ai = ai


    def quit(self):
        self._game_running = False
        self._command_send_queue.put(None)
        self._network.close()


    def _send_msg(self, msg):
        self._protocol.send_msg(msg)


    def _recv_msg(self):
        tmp = self._protocol.recv_msg()
        if tmp:
            return tmp
        log("Connection closed")
        self.quit()
        exit(0)


    def _send_command_thread(self):
        while True:
            msg = self._command_send_queue.get()
            if not msg:
                break
            if self._game_running:
                self._send_msg(msg)


    def connect(self):
        max_tries = Config.config['net']['max_tries']
        retry_waiting_time = Config.config['net']['retry_waiting_time']

        while True:
            log("Connecting to host '%s' port %s" % self._network.get_bind())
            try:
                self._network.connect()
                log("Connected successfully")
                return True
            except Exception as e:
                log("Failed to connect: %s" % e)

            max_tries -= 1
            if max_tries <= 0:
                break
            log("Reconnecting in %s seconds ..." % retry_waiting_time)
            sleep(retry_waiting_time)

        return False


    def join(self):
        if Config.config['general']['offline_mode']:
            join_msg = JoinOfflineGame(
                team_nickname = Config.config['ai']['team_nickname'],
                agent_name = Config.config['ai']['agent_name']
            )
        else:
            join_msg = JoinOnlineGame(
                token = Config.config['ai']['token'],
                agent_name = Config.config['ai']['agent_name']
            )

        self._send_msg(join_msg)
        while True:
            msg_type, client_joined_msg = self._recv_msg()
            if msg_type == ClientJoined.name():
                break

        if client_joined_msg.joined:
            self._ai.my_side = client_joined_msg.side_name
            self._ai.sides = client_joined_msg.sides
            self._ai.other_sides = list(self._ai.sides.keys())
            self._ai.other_sides.remove(self._ai.my_side)
            self._ai.other_side = self._ai.other_sides[0] if len(self._ai.other_sides) == 1 else None
            log("joined the game successfully")
            log("Side: %s" % client_joined_msg.side_name)
            return True

        log("Failed to join the game")
        return False


    def loop(self):
        while True:
            msg_type, msg = self._recv_msg()

            if isinstance(msg, BaseSnapshot):
                self._handle_snapshot(msg)

            elif msg_type == StartGame.name():
                self._handle_start_game(msg)

            elif msg_type == EndGame.name():
                self._handle_end_game(msg)
                break



    def _handle_snapshot(self, msg):
        self._ai.update(msg)
        if not self._game_running:
            self._game_running = True
            self._ai.initialize()
            if not Config.config['ai']['create_new_thread'] or self._ai.allowed_to_decide():
                Thread(target=self._ai.decide).start()
        elif Config.config['ai']['create_new_thread'] and self._ai.allowed_to_decide():
            Thread(target=self._ai.decide).start()


    def _handle_start_game(self, msg):
        Thread(target=self._send_command_thread).start()


    def _handle_end_game(self, msg):
        winner = msg.winner_sidename or 'draw'
        log("Winner side: %s" % winner)
        if msg.details:
            log("Details:")
            for name, sides in msg.details.items():
                log("  %s:" % name)
                for side, val in sides.items():
                    log("    %s -> %s" % (side, val))
        self.quit()
