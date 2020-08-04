'''
Creates an object where the game can be played manually, simulated, or otherwise experimented with
'''

from Deck import Deck
from Player import Player
from random import randint


def hand_busted(hand):
    """
    Takes all_cards of a player/dealer's hand and returns True if hand busts.
    Gets the sum of the initial value uses a value of 1 for Ace because
    we only care if lowest possible score is greater than 21)
    """
    sum_of_hand = sum([get_initial_value(card.rank) if card.rank != 'Ace' else 1 for card in hand])

    return sum_of_hand > 21


def get_initial_value(card_rank):
    # Returns the initial values of cards, because cards class values need to be overwritten
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
              'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    return values[card_rank]


def get_hand_score(cards):
    """Takes in a list of card objects and returns the maximum possible score of a hand or False if the hand has
     busted"""
    # Returns the maximum possible score of a hand or False if the hand has busted

    if hand_busted(cards):  # Busted hand value is set to False
        return False

    else:  # If no bust set value to highest possible score
        player_score = sum([get_initial_value(card.rank) for card in cards])

        while player_score > 21:  # Corrects initial scores for hands that contain an ace to their max possible score
            player_score -= 10

        return player_score


class BlackjackTable:

    def __init__(self, players, size_of_shoe=8):
        self.players = players  # A list of player objects
        self.dealer = Player('Dealer')
        self.shoe = Deck(size_of_shoe)
        self.discard_pile = [self.shoe.deal_one()]  # Always starts by burning one card
        self.cut_card_position = 104 + randint(-13, 13)  # Places a cut card 2 decks from the end +-1/4 deck

    def play_round_manually(self):
        """
        Returns the evaluation of game after simulating a manual "round" of blackjack. The returned object is a list
        equal to the number of players at the table with the possible values being True for a win, False for a loss,
        Blackjack for a 21 with 2 cards, and Push if there is a tie with the dealer.
        """
        needs_reset = len(self.shoe.all_cards) < self.cut_card_position

        if needs_reset:
            self.reset_shoe()

        self.deal_cards()
        self.player_draws_manually()
        self.dealer_draws()
        results = self.evaluate_game()
        print(results)
        self.discard_all_cards()
        return results

    def deal_cards(self, print_action=True):
        # deal two cards to each player and the dealer
        for _ in range(2):
            for player in self.players:
                player.add_card(self.shoe.deal_one())
            self.dealer.add_card(self.shoe.deal_one())

        if print_action:  # To keep from printing deal to console, pass False as parameter
            self.print_deal()

    def print_deal(self):
        for player in self.players:
            print(f'{player.name} has {player.all_cards[0]} & {player.all_cards[1]}')

        print(f"Dealer is showing a {self.dealer.all_cards[0]}.")

    def player_draws_manually(self):
        # Allows for each player to hit until bust or stand

        for player in self.players:

            while True:
                response = input(f'{player.name}, would you like to hit? (Y/N)').upper()

                # Hits
                if response == 'Y':
                    player.add_card(self.shoe.deal_one())
                    print(f'{player.name} drew a {player.all_cards[-1]}.')

                    # Busts
                    if hand_busted(player.all_cards):
                        print(f'{player.name} busts.')
                        break
                # Stays
                else:
                    break

    def player_hits(self, player):
        player.add_card(self.shoe.deal_one())

    def dealer_draws(self, print_action=True):
        # Dealer hits soft 17 and under. Can toggle off printing to console by passing in False as parameter

        if print_action:
            print(f'Dealer reveals {self.dealer.all_cards[1]}.')

        # Assigning initial values to the cards in hand
        value_of_dealer_cards = [get_initial_value(card.rank) for card in self.dealer.all_cards]

        # Dealer hits when they have less than 17 or a soft 17 (a 17 while holding at least 1 ace)
        while sum(value_of_dealer_cards) < 17 or (
                sum(value_of_dealer_cards) == 17 and 11 in value_of_dealer_cards):

            if print_action:
                print("Dealer hits.")

            self.dealer.add_card(self.shoe.deal_one())  # Dealers draws a card
            value_of_dealer_cards.append(get_initial_value(self.dealer.all_cards[-1].rank))

            if print_action:
                print(f"Dealer draws {self.dealer.all_cards[-1]}.")

            if hand_busted(self.dealer.all_cards):  # Dealer busts; break out of while loop
                if print_action:
                    print('Dealer busts.')
                break

            # Decrement the first ace in value_of_dealer_cards if the sum is over 21 but hand isn't busted
            if sum(value_of_dealer_cards) > 21:
                for x in range(len(value_of_dealer_cards)):
                    if value_of_dealer_cards[x] == 11:
                        value_of_dealer_cards[x] = 1
                        break

    def evaluate_game(self):
        """
        Returns a list equal to the number of players in game. The possible values of that list are True (winner),
        False (loser), 'Blackjack' (for 21 with 2 cards), or 'Push' (tie with dealer)
        """

        winners = [True for _ in range(len(self.players))]  # Assumes winners

        for x in range(len(self.players)):
            # Calls function which returns false for busted hand or integer of score
            winners[x] = get_hand_score(self.players[x].all_cards)

        dealer_value = get_hand_score(self.dealer.all_cards)

        for num in range(len(winners)):
            if winners[num] == False:  # Player Busted; Player Loses
                continue

            elif dealer_value == False:  # Player didn't bust, but dealer did; Player wins
                winners[num] = True

            elif winners[num] == 21 and len(self.players[num].all_cards) == 2:  # Check for player Blackjack
                winners[num] = 'Blackjack'

            else:  # Check for winner or push

                if winners[num] != dealer_value:  # Checks who has higher score if neither bust
                    winners[num] = winners[num] > dealer_value

                else:  # Push
                    winners[num] = 'Push'

        return winners

    def reset_shoe(self):
        # Put discarded cards back in shoe, shuffles, resets cut card, burns a card

        for x in range(len(self.discard_pile)):
            self.shoe.all_cards.append(self.discard_pile.pop())

        self.shoe.shuffle()
        self.cut_card_position = self.cut_card_position = 104 + randint(-13, 13)
        self.discard_pile.append(self.shoe.deal_one())

    def clear_table_cards(self):

        for x in range(len(self.dealer.all_cards)):
            self.discard_pile.append(self.dealer.remove_one())

        for player in self.players:
            for y in range(len(player.all_cards)):
                self.discard_pile.append(player.remove_one())