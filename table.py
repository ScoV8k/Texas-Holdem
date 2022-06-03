from deck import Deck
from player import Player
from bot import Bot
import time

class Table:
    def __init__(self, list_of_players):
        self.cards = []
        self.pot = 0
        self.turn_token_amount = 0
        self.list_of_players = list_of_players
        self.active_players = []
        self.deck = Deck()
        self._round = 0
        self.turn = 0
        self.small_blind = None
        self.big_blind = None
        self.figure_dictionary = {1: "Wysoką kartę", 2: "Parę", 3: "Dwie pary", 4: "Trójkę", 5: "Strita",
                     6: "Kolor", 7: "Fulla", 8: "Karetę", 9: "Pokera"}

    def get_cards(self):
        return self.cards

    def get_list_of_players(self):
        return self.list_of_players

    def get_active_players(self):
        return self.active_players

    def set_active_players(self, list_of_players):
        self.active_players = list_of_players

    def pot_add(self, number):
        self.pot += number

    def reset_pot(self):
        self.pot = 0

    def players_raise(self, raise_number):
        all_number = raise_number + self.turn_token_amount
        self.pot_add(all_number)
        self.turn_token_amount += raise_number


    def add_card(self, card):
        self.cards.append(card)

    def show_deck(self):
        self.deck.show_all_cards()
        print(len(self.deck.deck()))

    def round(self):
        self.reset_pot()
        self.clear_all_gave_tokens()
        self.clear_all_in()
        self.deck = Deck()
        self.active_players = list(self.get_list_of_players())
        self.generate_bluffs()
        self.clear_figures()
        self.set_blinds()
        cards = ""
        self.deck.shuffle()
        for player in self.active_players:
            player.add_card(self.deck.deal())
            player.add_card(self.deck.deal())
        for i in range(4):
            self.set_figures()
            ###
            if self.turn < 4 and self.turn != 0:
                print("\n\n\nRozdanie: " + str(i))
                if self.turn == 1:
                    self.add_card(self.deck.deal())
                    self.add_card(self.deck.deal())
                    self.add_card(self.deck.deal())
                else:
                    self.add_card(self.deck.deal())
                self.clear_all_gave_tokens()
                self.turn_token_amount = 0
                self.set_figures()
                if len(self.get_cards()) == 3:
                    for card in self.get_cards():
                        cards += str(card) + ' '
                else:
                    cards += str(self.get_cards()[-1]) + ' '
                print("Karty na stole: " + cards)
            print("\n")

            self.turn += 1
            while True:
                for j in range(len(self.active_players)):
                    player = self.active_players[(j+self._round+2) % len(self.active_players)]
                    if player.get_gave_tokens() != self.turn_token_amount and player.get_gave_tokens() != -1 and player.get_all_in() == 0:
                        if not isinstance(player, Bot):
                            #### wybór gracza

                            print("\nTwoje karty: ", player.show_cards(), "\n")
                            print("Masz ", player.get_tokens(), " żetonów\n")
                            print("Aktualny bet: ", self.turn_token_amount)
                            print("\nPULA: ", self.pot)
                            if self.turn_token_amount == 0:
                                print("1-sprawdzam\n2-podbijam\n3-pasuje\n")
                            else:
                                print("1-dobijam\n2-podbijam\n3-pasuje\n")
                            while True:
                                try:
                                    choice = input("Wybierz co chcesz zrobić: ")
                                    if self.turn_token_amount == 0:
                                        if choice == "1":
                                            player.check()
                                            print('\n')
                                            break
                                    else:
                                        if choice == "1":
                                            player.take_tokens(self.turn_token_amount)
                                            player.set_gave_tokens(self.turn_token_amount)
                                            self.pot_add(self.turn_token_amount)
                                            if player.get_tokens() == 0:
                                                player.set_all_in(1)
                                            print('\n')
                                            break
                                    if choice == "2":
                                        print("Masz ", player.get_tokens(), " żetonów")
                                        if player.get_gave_tokens() == None:
                                            gave = 0
                                        else:
                                            gave = player.get_gave_tokens()
                                        if gave != 0:
                                            print("Już postawione żetony: ", player.get_gave_tokens())
                                        while True:
                                            try:
                                                number = int(input("Ile chcesz postawić: "))
                                                no_gave_value = number - gave
                                                if ((no_gave_value) > player.get_tokens() or number < self.turn_token_amount) and number != player.get_tokens():          # dodać jeśli mniejsze niż podbicie
                                                    print("Niepoprawna ilość żetonów")
                                            except ValueError:
                                                print("Niepoprawna ilość żetonów")
                                            else:
                                                self.pot_add(no_gave_value)
                                                self.turn_token_amount = number
                                                player.take_tokens(no_gave_value)
                                                player.set_gave_tokens(number)
                                                if player.get_tokens() == 0:
                                                    player.set_all_in(1)
                                                print('\n')
                                                break
                                        break
                                    elif choice == "3":
                                        self.active_players.remove(player)
                                        print('\n')
                                        break
                                    else:
                                        print("wybierz poprawną opcję")
                                        continue
                                except ValueError:
                                    if player.get_gave_tokens() == None:
                                        gave = 0
                                    else:
                                        gave = player.get_gave_tokens()
                                    player.set_gave_tokens(gave + player.get_tokens())
                                    player.take_tokens(player.get_tokens())
                                    self.pot_add(player.get_tokens())
                                    player.set_all_in(1)
                                    break
                                ####
                        else:
                            print(player.get_name() + " (" + str(player.get_tokens()) + "): ", end="")
                            try:
                                move = player.move(self.turn_token_amount)
                                time.sleep(1)
                                if move == 0:
                                    print('pasuje')
                                if isinstance(move, tuple):
                                    if move[0] == 2:
                                        self.pot_add(move[1])
                                        print('dobijam')
                                    if move[0] == 3:
                                        if player.get_gave_tokens() == None:
                                            gave = 0
                                        else:
                                            gave = player.get_gave_tokens()
                                        self.pot_add(self.turn_token_amount + move[1] - gave)
                                        self.turn_token_amount += move[1]
                                        player.set_gave_tokens(self.turn_token_amount)
                                        print(f'podbijam o {move[1]}')
                                if move == 1:
                                    print('czekam')
                                if player.get_tokens() == 0:
                                    player.set_all_in(1)
                            except ValueError:
                                print("all in")
                                if player.get_gave_tokens() == None:
                                    gave = 0
                                else:
                                    gave = player.get_gave_tokens()
                                player.take_tokens(player.get_tokens())
                                player.set_gave_tokens(gave + player.get_tokens())
                                self.pot_add(player.get_tokens())
                                player.set_all_in(1)
                x = 0
                new_list = []
                for player in self.active_players:
                    if player.get_gave_tokens() != -1:
                        new_list.append(player)
                self.active_players = new_list
                for player in self.active_players:
                    if player.get_gave_tokens() != self.turn_token_amount and player.get_all_in() != 1:
                        x = 1
                if x == 0:
                    break
                if len(self.active_players) == 1:
                    break

            if len(self.active_players) == 1:
                break

        print("Karty na stole: " + cards)
        print("Zwycięska pula: " + str(self.pot))
        winner = self.choose_winner()
        self.give_winner_pot(winner)
        self.winner_print(winner)
        self.clear_all_cards()
        lost = self.remove_lost_players()
        for player in lost:
            print(f'{player.get_name()} opuszcza stół')
        self.turn = 0
        self._round += 1

    def set_blinds(self):
        self.small_blind = self.active_players[self._round%len(self.active_players)]
        self.big_blind = self.active_players[((self._round + 1)%len(self.active_players))]
        self.small_blind.take_tokens(5)
        self.big_blind.take_tokens(10)
        self.small_blind.set_gave_tokens(5)
        self.big_blind.set_gave_tokens(10)
        self.turn_token_amount = 10
        self.pot_add(15)
        print("Small blind: ", self.small_blind.get_name())
        print("Big blind: ", self.big_blind.get_name())

    def clear_all_cards(self):
        self.cards = []
        for player in self.list_of_players:
            player.clear_cards()

    def clear_all_gave_tokens(self):
        for player in self.list_of_players:
            player.set_gave_tokens(None) # 0

    def clear_all_in(self):
        for player in self.list_of_players:
            player.set_all_in(0)

    def remove_lost_players(self):
        lost_players = []
        stay_players = []
        for player in self.list_of_players:
            if player.get_tokens() != 0:
                stay_players.append(player)
            else:
                lost_players.append(player)
        self.list_of_players = stay_players
        return lost_players


    def give_winner_pot(self, winner):
        if isinstance(winner, list):
            for player in winner:
                player.add_tokens(self.pot // len(winner))
        else:
            winner.add_tokens(self.pot)

    def winner_print(self, winner):
        if isinstance(winner, list):
            win_text = ""
            for player in winner:
                win_text += player.get_name() + " " + player.show_cards() + ", "
            print("Wygrali: ", win_text[:-2])
        else:
            print("Wygrał: ", winner.get_name().title())
            if winner.get_figure() != None:
                print("Mając: ", self.figure_dictionary[winner.get_figure()], " ", winner.show_cards())
            print("\n\n")


    def choose_winner(self):
        max_figure = 0
        max_figure_value = 0
        best_figure_list = []
        winners = []
        if len(self.active_players) == 1:
            return self.active_players[0]
        for player in self.active_players:
            max_figure = max(max_figure, player.get_figure())
        for player in self.active_players:
            if player.get_figure() == max_figure:
                best_figure_list.append(player)
        if len(best_figure_list) == 1:
            return best_figure_list[0]      #zwraca gracza jeśli wygral jeden
        else:
            for player in best_figure_list:
                max_figure_value = max(max_figure_value, player.get_figure_value())
            for player in best_figure_list:
                if player.get_figure_value() == max_figure_value:
                    winners.append(player)
            if len(winners) == 1:
                return winners[0]  #zwraca gracza jeśli wygrał jeden
            else:
                return winners # zwraca liste graczy jeśli wygrało kilku




# 1 - karta, !2 - para, !3 - dwie pary, !4 - trójka, 5 - strit, !6 - kolor, !7 - full, !!8 - czwórka, 9 - poker, 10 - poker królewski

    def set_figures(self):
        for player in self.active_players:
            cards = self.cards + player.get_cards()
            values = [card.value() for card in cards]
            suits = [card.suit() for card in cards]
            values.sort()
            scorer = PokerFigure(cards)
            score = scorer.pairs_tripe_full_four()
            colour = scorer.colour()
            straight = scorer.straight()
            poker = scorer.poker()
            highest_card = scorer.high_card()
            player.set_figure(1)
            player.set_figure_value(highest_card)
            if score != 0:
                player.set_figure(score[0])
                player.set_figure_value(score[1])
            if player.get_figure() < 6:
                if straight != 0:
                    player.set_figure(straight[0])
                    player.set_figure_value(straight[1])
            if colour != 0:
                player.set_figure(colour[0])
                player.set_figure_value(colour[1])
            if poker != 0:
                player.set_figure(poker[0])
                player.set_figure_value(poker[1])

    def clear_figures(self):
        for player in self.list_of_players:
            player.set_figure(None)
            player.set_figure_value(None)

    def generate_bluffs(self):
        for player in self.active_players:
            if isinstance(player, Bot):
                player.generate_bluff()




class PokerFigure():
    def __init__(self, cards):
        self._cards = cards
        self._values = [card.value() for card in self._cards]
        self._suits = [card.suit() for card in self._cards]

    def pairs_tripe_full_four(self):
        multiple_values = set()
        multiple_values3 = set()
        multiple_values4 = set()
        for value in self._values:
            if self._values.count(value) == 2:  #jeśli para wrzuca do m_v
                multiple_values.add(value)
            if self._values.count(value) == 3: #jeśli trójka wrzuca do m_v3
                multiple_values3.add(value)
            if self._values.count(value) == 4: #jeśli czwórka wrzuca do m_v4
                multiple_values4.add(value)
        if len(multiple_values) >=1 and len(multiple_values3) == 1: # Full
            return (7, (max(multiple_values) * 2) + sum(multiple_values3) *3)
        if len(multiple_values) == 1: # para
            return (2, sum(multiple_values))
        if len(multiple_values) == 2: # 2 pary
            return (3, sum(multiple_values))
        if len(multiple_values3) == 1: # trójka
            return (4, sum(multiple_values3))
        if len(multiple_values3) == 2: # 2 trójki = Full
            return (7, (max(multiple_values3) * 4) + (min(multiple_values3) * 2))
        if len(multiple_values4) == 1: # kareta
            return (8, sum(multiple_values4))
        return 0

    def colour(self):
        color_cards = []
        color = 0
        for suit in self._suits:
            if self._suits.count(suit) == 5:
                color = suit
                break
        if color != 0:
            for card in self._cards:
                if card.suit() == color:
                    color_cards.append(card.value())
            if color_cards != []:
                return (6, sum(color_cards))
        return 0

    def straight(self):
        a = 0
        biggest = 0
        values = self._values
        values.sort()
        if values != None:
            for i in range(len(values)-1):
                if values[i] + 1 == values[i+1]:
                    a += 1
                    biggest = values[i+1]
                elif values[i] == values[i+1]:
                    pass
                else:
                    a = 0
                    biggest = 0
            if a >= 4:
                return (5, biggest)
        return 0


    def poker(self):
        a = 0
        biggest = 0
        values = self._values
        suits = self._suits
        zipped = list(zip(values, suits))
        zipped.sort()
        if zipped != None:
            for i in range(len(zipped)-1):
                if (zipped[i][0] + 1 == zipped[i+1][0]) and (zipped[i][1] == zipped[i+1][1]):
                    a += 1
                    biggest = zipped[i+1][0]
                elif zipped[i][0] == zipped[i+1][0]:
                    pass
                else:
                    a = 0
                    biggest = 0
            if a >= 4:
                return (9, biggest)
        return 0

    def high_card(self):
        return max(self._values)
