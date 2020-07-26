from Deck import Deck
from Player import Player
from copy import deepcopy

shoe = Deck()
copy_of_shoe = deepcopy(shoe)
for x in range(1,4):
    print(f'shoe: {shoe.deal_one()}')
    print(f' cpy_shoe: {copy_of_shoe.all_cards[-x]}')

for y in range(1,4):
    print(f'shoe: {shoe.all_cards[-y]}')
    print(f' cpy_shoe: {copy_of_shoe.all_cards[-y]}')
