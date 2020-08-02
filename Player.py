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
        return self.all_cards.pop()

    def __str__(self):
        cards = [str(x) for x in self.all_cards]
        return f"{self.name} has {cards}"
