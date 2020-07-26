'''
Creates a standard deck of 52 playing cards
'''
import Card
import random

class Deck:

    def __init__(self):
        self.all_cards = []

        for suit in Card.suits:
            for rank in Card.ranks:
                created_card = Card.Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def print_deck(self):
        for x in self.all_cards:
            print(x)

    def deal_one(self):
        return self.all_cards.pop()