# -*- coding: utf-8 -*-

# python imports
import random

# chillin imports
from chillin_client import RealtimeAI

# project imports
from ks.commands import Move, Bomb, EDir
from ks.models import ECellType


class AI(RealtimeAI):

    def __init__(self, world):
        super(AI, self).__init__(world)

        self.directions = [EDir.Top, EDir.Right, EDir.Bottom, EDir.Left]


    def decide(self):
        print ('decide')

        cmd_rand = random.uniform(0.0, 1.0)
        if cmd_rand < 0.9: # Move
            bomberman = self.world.bombermans[self.my_side]
            valid_directions = []

            if self.world.board[bomberman.y - 1][bomberman.x].type == ECellType.Empty:
                valid_directions.append(EDir.Top)
            if self.world.board[bomberman.y][bomberman.x + 1].type == ECellType.Empty:
                valid_directions.append(EDir.Right)
            if self.world.board[bomberman.y + 1][bomberman.x].type == ECellType.Empty:
                valid_directions.append(EDir.Bottom)
            if self.world.board[bomberman.y][bomberman.x - 1].type == ECellType.Empty:
                valid_directions.append(EDir.Left)

            if len(valid_directions) >= 1:
                self.send_command(Move(direction=valid_directions[random.randrange(0, len(valid_directions))]))
        else: # Bomb
            self.send_command(Bomb())
