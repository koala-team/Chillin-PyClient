# -*- coding: utf-8 -*-

# project imports
from .config import Config
from .core import Core
from .ais import BaseAI, RealtimeAI, TurnbasedAI


class GameClient:
    
    def __init__(self, gamecfg_path):
        Config.initialize(gamecfg_path)
        self._core = Core()


    def register_ai(self, ai):
        self._core.register_ai(ai)


    def run(self):
        if not self._core.connect():
            return
        if not self._core.join():
            return
        self._core.loop()
