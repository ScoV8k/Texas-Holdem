from card import Card
from deck import Deck
from player import Player
import random


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)
        self._bluff = random.randint(0, 20)

    def move(self, turn_tokens):
        if self._gave_tokens == None:
            gave = 0
        else:
            gave = self._gave_tokens
        if self._bluff == 1:
            if turn_tokens <= 100:
                raise_num = random.choice([50, 100])
                self.take_tokens(turn_tokens + raise_num - gave)
                return (3, raise_num)
            else:
                self.take_tokens(turn_tokens - gave) # dobija
                value = (2, turn_tokens - gave)
                self.set_gave_tokens(turn_tokens)
                return value
        if turn_tokens == 0:
            if self.get_figure() >= 3 and random.randint(1, 5) == 1:
                raise_num = random.randint(1, 5) * 10
                self.take_tokens(turn_tokens + raise_num - gave)
                return (3, raise_num)
            self.check()
            return 1
        elif self.get_figure() >= 7:
            if turn_tokens <= 350:
                if random.randint(1, 3) == 1:
                    self.take_tokens(turn_tokens - gave) # dobija
                    value = (2, turn_tokens - gave)
                    self.set_gave_tokens(turn_tokens)
                    return value
                else:
                    value = random.randint(1, 2) * 100
                    self.take_tokens(turn_tokens + value - gave)
                    return (3, value)
            self.take_tokens(turn_tokens - gave) # dobija
            value = (2, turn_tokens - gave)
            self.set_gave_tokens(turn_tokens)
            return value


        elif self.get_figure() >=3:
            if turn_tokens <= 100:
                if random.randint(1, 2) == 1:
                    self.take_tokens(turn_tokens - gave) # dobija
                    value = (2, turn_tokens - gave)
                    self.set_gave_tokens(turn_tokens)
                    return value
                else:
                    value = random.randint(1, 5) * 10
                    self.take_tokens(turn_tokens + value - gave)
                    return (3, value)
            if self.get_figure() >= 5:
                self.take_tokens(turn_tokens - gave) # dobija
                value = (2, turn_tokens - gave)
                self.set_gave_tokens(turn_tokens)
                return value
            else:
                self.set_gave_tokens(-1)
                return 0 # Pass, remove this player
        elif self.get_figure() == 2:
            if turn_tokens <= 100:
                self.take_tokens(turn_tokens - gave) # dobija
                value = (2, turn_tokens - gave)
                self.set_gave_tokens(turn_tokens)
                return value
            else:
                self.set_gave_tokens(-1)
                return 0 # Pass, remove this player
        else:
            if turn_tokens > 20:
                self.set_gave_tokens(-1)
                return 0 # Pass, remove this player
            self.take_tokens(turn_tokens - gave) # dobija
            value = (2, turn_tokens - gave)
            self.set_gave_tokens(turn_tokens)
            return value


    def generate_bluff(self):
        self._bluff = random.randint(0, 20)

    def zero_bluff(self):
        self._bluff = 0
