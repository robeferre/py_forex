import random
import pdb
from datetime import datetime
from dateutil.parser import parse
from event import OrderEvent


class TestRandomStrategy(object):
    def __init__(self, instrument, units, events):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.range = list()

    def crazy_signal(self, price_range):
        """
        This is a test of a crazy idea
        :param price_range:
        :return:
        """
        for y in ["ask", "bid"]:
            index = 0
            earlier_pos = 0
            for x in price_range[::-1]:
                if index == 0:
                    earlier_pos = x[0]
                    index += 1
                    continue
                if y == "ask":
                    if earlier_pos < x[0]:
                        break
                    else:
                        print("### SIGNAL ASK STEP %s ###" % index)
                        index += 1
                        earlier_pos = x[0]
                        if index == 10:
                            return "buy"
                        else:
                            continue
                else:
                    if earlier_pos > x[0]:
                        break
                    else:
                        print("### SIGNAL BID STEP %s ###" % index)
                        index += 1
                        earlier_pos = x[0]
                        if index == 10:
                            return "bid"
                        else:
                            continue
        return False

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            time = parse(event.time)
            time = ('%02d:%02d.%d' % (time.minute, time.second, time.microsecond))
            ask_time = [event.ask, time]
            self.range.append(ask_time)
            if len(self.range) == 11:
                self.range.pop(0)
                action = self.crazy_signal(self.range)
                if action:
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print("$$$$$$$$$$$$$$$$  SINAL %s $$$$$$$$$$$$$$$$$$$$" % action)
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
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
