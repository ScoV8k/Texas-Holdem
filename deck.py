from card import Card
import random

class Deck:
    def __init__(self):
        self._deck = []
        [[self._deck.append(Card(value, suit)) for suit in Card.suits] for value in Card.values]

    def deck(self):
        return self._deck

    def remove_card(self, card):
        for item in self._deck:
            if item == card:
                self._deck.remove(item)

    def deal(self):
        return self._deck.pop()


    def shuffle(self):
        random.shuffle(self._deck)


    def show_all_cards(self):
        cards = ''
        for card in self._deck:
            cards += str(card) + '\n'
        return cards