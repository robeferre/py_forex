import random
import pdb

from event import OrderEvent


class TestRandomStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.range = list()

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            self.range.append(event.ask)
            if len(self.range) == 10:
                self.range.pop(0)
                print(self.range)
            else:
                print(self.range)


            # if self.ticks % 10 == 0:
            #     pdb.set_trace()
            #
            #     side = random.choice(["buy", "sell"])
            #     order = OrderEvent(
            #         self.instrument, self.units, "market", side
            #     )
            #     self.events.put(order)
            #     self.range = list()