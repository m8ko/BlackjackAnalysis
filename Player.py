'''
Represents a player of the game
'''


class Player:

    def __init__(self, name='Default'):
        self.name = name
        self.all_cards = []

    def add_card(self, card):

        #multiple card objects
        if type(card) == type([]):
            self.all_cards.extend(card)

        #single card object
        else:
            self.all_cards.append(card)

    def remove_one(self):
        return self.all_cards.pop(0)

    def discard_all_cards(self):
        discarded = []

        for _ in range(len(self.all_cards)):
            discarded.append(self.remove_one())

        return discarded

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)} cards.'
