# -*- coding: utf-8 -*-

# project imports
from .helpers.parser import Parser
from .helpers.messages import BaseCommand, RealtimeCommand, TurnbasedCommand


class BaseAI(object):

    def __init__(self, world):
        self._command_send_queue = None
        self.world = world
        self.sides = None
        self.my_side = None


    def set_command_send_queue(self, q):
        self._command_send_queue = q


    def update(self, snapshot):
        self.world.deserialize(Parser.get_bytes(snapshot.world_payload))


    def allowed_to_decide(self):
        return True


    def _send_command(self, command, msg=None):
        if not msg:
            msg = BaseCommand()
        msg.type, msg.payload = Parser.get_tuplestring(command)
        self._command_send_queue.put(msg)


    def send_command(self, command):
        if self.allowed_to_decide():
            self._send_command(command)


    def decide(self):
        pass



class RealtimeAI(BaseAI):

    def __init__(self, world):
        super(RealtimeAI, self).__init__(world)
        self.current_cycle = 0
        self.cycle_duration = None


    def update(self, snapshot):
        super(RealtimeAI, self).update(snapshot)
        self.current_cycle = snapshot.current_cycle
        self.cycle_duration = snapshot.cycle_duration


    def allowed_to_decide(self):
        return True


    def _send_command(self, command, msg=None):
        if not msg:
            msg = RealtimeCommand()
        msg.cycle = self.current_cycle
        super(RealtimeAI, self)._send_command(command, msg)



class TurnbasedAI(RealtimeAI):

    def __init__(self, world):
        super(TurnbasedAI, self).__init__(world)
        self.turn_allowed_sides = []


    def update(self, snapshot):
        super(TurnbasedAI, self).update(snapshot)
        self.turn_allowed_sides = snapshot.turn_allowed_sides


    def allowed_to_decide(self):
        return self.my_side in self.turn_allowed_sides


    def _send_command(self, command, msg=None):
        if not msg:
            msg = TurnbasedCommand()
        super(TurnbasedAI, self)._send_command(command, msg)
