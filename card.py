class Card:
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = ["♥","♦", "♠", "♣" ]

    def __init__(self, value, suit):
        self._value = value
        self._suit = suit

    def value(self):
        return self._value

    def suit(self):
        return self._suit

    def __repr__(self):
        suit = self._suit
        if self._value == 11:
            value = 'Jack'
        elif self._value == 12:
            value = 'Queen'
        elif self._value == 13:
            value = 'King'
        elif self._value == 14:
            value = 'As'
        else:
            value = str(self._value)
        return value + suit

    def __str__(self):
        suit = self._suit
        if self._value == 11:
            value = 'Jack'
        elif self._value == 12:
            value = 'Queen'
        elif self._value == 13:
            value = 'King'
        elif self._value == 14:
            value = 'As'
        else:
            value = str(self._value)
        return value + suit

    def __eq__(self, other):
        return (
            self._value == other._value and
            self._suit == other._suit
        )
