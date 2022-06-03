import random

random.sample

class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []
        self._tokens = 1000
        self._figure = None
        self._figure_value = None
        self._gave_tokens = 0
        self._all_in = 0

    def get_name(self):
        return self._name

    def get_tokens(self):
        return self._tokens

    def get_figure(self):
        return self._figure

    def get_figure_value(self):
        return self._figure_value

    def get_cards(self):
        return self._cards

    def get_gave_tokens(self):
        return self._gave_tokens

    def get_all_in(self):
        return self._all_in

    def set_all_in(self, number):
        self._all_in = number

    def set_figure(self, figure):
        self._figure = figure

    def set_figure_value(self, figure_value):
        self._figure_value = figure_value

    def set_gave_tokens(self, new_tokens):
        self._gave_tokens = new_tokens

    def add_card(self, card):
        self._cards.append(card)

    def show_cards(self):
        text = "(" + str(self.get_cards()[0]) + ", " + str(self.get_cards()[1]) + ")"
        return text

    def clear_cards(self):
        self._cards = []

    def check(self):
        self.set_gave_tokens(0)

    def take_tokens(self, number):
        if (self._tokens - number) < 0:
            raise ValueError
        self._tokens -= number

    def add_tokens(self, number):
        self._tokens += number

