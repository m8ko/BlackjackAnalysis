from Player import Player
from Deck import Deck

number_of_decks = 8
hit_score_probability = [[num for num in range(4, 22)]]

card_value_count = dict([(x, 4 * number_of_decks) for x in range(1, 12)])
card_value_count[10] = number_of_decks * 4 * 4

print(hit_score_probability)

# Columns represent possible scores. Rows represent current score
for x in range(4, 22):
    row = []
    row.append(x)
    for y in range(4, 22):

        # impossible value (ignoring possibility of ace in current hand)
        if y <= x or y-x>11:
            row.append(0)

        # controls for Ace being 2 possible values. Only cares about probability of getting 11 (not 1) if 11 doesn't
        # bust the hand
        elif y-x == 1 and x+11 <= 21:
            row.append(0)

        # looks up number needed (y-x) to get the possible score (y) and calcs possibility
        else:
            row.append( card_value_count[y-x] / (52*number_of_decks))
    hit_score_probability.append(row)

for rows in hit_score_probability:
    for value in rows:
        print(value, end=",")
    print()