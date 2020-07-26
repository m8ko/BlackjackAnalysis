'''
Simulates a game of blackjack
'''

from Deck import Deck
from Player import Player


def play_round():
    deal_cards()
    print_deal()
    player_draws()
    dealer_draws()
    print(evaluate_game())


def deal_cards():
    # deal 2 cards to each player and the dealer
    for _ in range(2):
        for player in players:
            player.add_card(shoe.deal_one())
        dealer.add_card(shoe.deal_one())


def print_deal():
    for player in players:
        print(f'{player.name} has {player.all_cards[0]} & {player.all_cards[1]}')

    print(f"Dealer is showing a {dealer.all_cards[0]}.")


def player_draws():
    for player in players:

        while True:
            response = input(f'{player.name}, would you like to hit? (Y/N)').upper()

            # Hits
            if response == 'Y':
                player.add_card(shoe.deal_one())
                print(f'{player.name} drew a {player.all_cards[-1]}.')

                # Busts
                if hand_busted(player.all_cards):
                    print(f'{player.name} busts.')
                    break
            # Stays
            else:
                break


# Takes all_cards of a player/dealer's hand and returns True if hand busts
def hand_busted(hand):
    '''
    Gets the sum of the initial value uses a value of 1 for Ace because
    we only care if lowest possible score is greater than 21)
    '''
    sum_of_hand = sum([get_initial_value(card.rank) if card.rank != 'Ace' else 1 for card in hand])

    return sum_of_hand > 21


def dealer_draws():
    print(f'Dealer reveals {dealer.all_cards[1]}.')

    # Assigning initial values to the cards in hand
    value_of_dealer_cards = [get_initial_value(card.rank) for card in dealer.all_cards]

    # Dealer hits when they have less than 17 or a soft 17 (a 17 while holding at least 1 ace)
    while sum(value_of_dealer_cards) < 17 or (
            sum(value_of_dealer_cards) == 17 and 11 in value_of_dealer_cards):

        print("Dealer hits.")
        # Dealers draws a card
        dealer.add_card(shoe.deal_one())
        value_of_dealer_cards.append(get_initial_value(dealer.all_cards[-1].rank))
        print(f"Dealer draws {dealer.all_cards[-1]}.")

        # Dealer busts; break out of while loop
        if hand_busted(dealer.all_cards):
            print('Dealer busts.')
            break

        # Decrement the first ace in value_of_dealer_cards if the sum is over 21 but hand isn't busted
        if sum(value_of_dealer_cards) > 21:
            for x in range(len(value_of_dealer_cards)):
                if value_of_dealer_cards[x] == 11:
                    value_of_dealer_cards[x] = 1
                    break


# Returns the initial values of cards; Ace defaults to 11
def get_initial_value(card_rank):
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
              'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    return values[card_rank]


def evaluate_game():
    """
    Returns a list equal to the number of players in game. The possible values of that list are True (winner),
    False (loser), 'Blackjack' (for 21 with 2 cards), or 'Push' (tie with dealer)
    """

    # Assumes winners
    winners = [True for _ in range(len(players)+1)]

    players.append(dealer)
    for x in range(len(players)):

        # Busted hand value is set to False
        if hand_busted(players[x].all_cards):
            winners[x] = False

        # If no bust set value to highest possible score
        else:
            player_score = sum([get_initial_value(card.rank) for card in players[x].all_cards])

            # Corrects initial scores for hands that contain an ace to their max possible score
            while player_score > 21:
                player_score -= 10
            winners[x] = player_score

    # Get the value evaluation of dealer and pop it from player list
    dealer_value = winners.pop()
    players.pop()

    for num in range(len(winners)):
        # Player Busted; Player Loses
        if winners[num] == False:
            continue

        # Player didn't bust, but dealer did; Player wins
        elif dealer_value == False:
            winners[num] = True

        # Check for player Blackjack; Player wins
        elif winners[num] == 21 and len(players[num].all_cards) == 2:
            winners[num] = 'Blackjack'

        # Check for winner or push
        else:
            # Checks who has higher score if neither bust
            if winners[num] != dealer_value:
                winners[num] = winners[num] > dealer_value

            # Push
            else:
                winners[num] = 'Push'

    return winners



shoe = Deck()
shoe.shuffle()

player_one = Player('Anthony')
player_two = Player('Niki')
dealer = Player('Dealer')

# list of players
players = [player_one,player_two]

play_round()
