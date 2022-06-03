from player import Player
from table import Table
from bot import Bot


class Poker:
    def __init__(self):
        Adam = Bot("Adam")
        Jan = Bot("Jan")
        Grzegorz = Bot("Grzegorz")
        Władysław = Bot("Władysław")
        Dominik = Bot("Dominik")
        Andrzej = Bot("Andrzej")
        You = Player("Ty")
        self.table = Table([Adam, Jan, Grzegorz, Władysław, Dominik, Andrzej, You])

    def start(self):
        print("1-Start game\n2-Exit")
        while True:
            a = input()
            if a == '1':
                self.table.round()
                while True:
                    print("1-Następna runda\n2-Exit")
                    b = input()
                    if b == '1':
                        self.table.round()
                    if b == '2':
                        break
                break
            elif a =='2':
                break



game = Poker()
game.start()







