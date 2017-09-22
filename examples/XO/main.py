#! /usr/bin/env python
# -*- coding: utf-8 -*-

# python imports
import sys

# chillin imports
from chillin_client import GameClient

# project imports
from ai import AI
from ks.models import World


ai = AI(World())

app = GameClient(sys.argv[1])
app.register_ai(ai)
app.run()
