# -*- coding: utf-8 -*-

# chillin imports
from chillin_client import TurnbasedAI

# project imports
from ks.commands import Place
from ks.models import ECell


class AI(TurnbasedAI):

    def decide(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.world.board[i][j] == ECell.Empty:
                    self.send_command(Place(x=j, y=i))
                    return
