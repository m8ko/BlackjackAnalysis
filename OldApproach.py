from Player import Player
from BlackjackTable import BlackjackTable, get_hand_score, hand_busted
from copy import deepcopy
from random import randint
from pprint import pprint
import numpy as np
import pandas as pd

"""
results will be stored in a 2d list of nested dictionaries.
The nested dictionary is = {"Hit": {'Win': 0, 'Loss': 0, 'Draw': 0}, "Stand": {'Win': 0, 'Loss': 0, 'Draw': 0}} .
The column index represent the dealer scores.
The row index represents player scores.
    ex. To access the number of times a player won by standing on a 17 vs a dealer showing 10
        results_matrix[17][10]['Stand']['Win']
"""

results_matrix = [
    [{"Hit": {'Win': 0, 'Loss': 0, 'Draw': 0}, "Stand": {'Win': 0, 'Loss': 0, 'Draw': 0}} for i in range(11)] for y in
    range(21)]

sim_table = BlackjackTable([Player('Player1')])
sim_table.shoe.shuffle()


def run_game_simulation(number_of_rounds):
    for _ in range(number_of_rounds):

        needs_reset = len(sim_table.shoe.all_cards) < sim_table.cut_card_position

        if needs_reset:
            sim_table.reset_shoe()

        sim_table.deal_cards()

        """
        # with a deep copy of the table, simulate standing and store result
        """
        simulate_stand(deepcopy(sim_table))

        # Simulates player hitting once sim_table_copy object and adds result to matrix

        simulate_hit(sim_table)

        # Randomly chose which instance of sim_table to go forward with

        # sim_table.player_draws_manually()
        # sim_table.dealer_draws()
        # results = self.evaluate_game()
        # self.discard_all_cards()
        # return results


def store_results(dlr_score, player_tuples):
    """
    Takes in dlr_score (dealer score), a list of tuples representing the players' score, action, and results
    the stores each player results in the results matrix.

    The player_tuple object is as follows:
        [(player1 result tuple), (player2 result tuple),...((playerN result tuple)]

    The player result tuple is as follows:
        (Hand score prior to action, action, result)
        e.x.
            (17, "Stand", True)
            The player had a 17, stood on the hand, and beat the dealer
            (7, "Hit", False)
            The player had a 7, hit their hand, and lost to the dealer
    """

    for x in range(len(player_tuples)):
        player_score, action, result = player_tuples[x]

        # player wins or blackjack
        if result == True or result == 'Blackjack':
            results_matrix[player_score - 1][dlr_score - 1][action]['Win'] += 1

        # player loses
        elif not result:
            results_matrix[player_score - 1][dlr_score - 1][action]['Loss'] += 1

        # Draws with dealer
        else:
            results_matrix[player_score - 1][dlr_score - 1][action]['Draw'] += 1


def simulate_stand(table):
    """
    Accepts a Simulates a player standing on hand using table object and adds the result to the matrix
    """

    for player in table.players:
        print(f"{player.name} stands with a {get_hand_score(player.all_cards)}")

    table.dealer_draws()

    # Get score of dealers up card and list of player scores
    dealer_score = get_hand_score(table.dealer.all_cards[0:1])
    print(dealer_score)
    player_scores = [get_hand_score(table.players[x].all_cards) for x in range(len(table.players))]
    player_results = table.evaluate_game()

    player_result_tuples = list(zip(player_scores, ['Stand' for y in range(len(player_scores))], player_results))

    print(player_result_tuples)

    store_results(dealer_score, player_result_tuples)


def simulate_hit(table):
    """
    I think that this has to be a recursive method which stores a sum total of 1 for the root node distributed
    to each outcome based on the results of the subsequent nodes.
    Example 1:
        player has: 12
        dealer showing: 8 (has a 10 face down)

        The next three cards in the shoe are all threes.

        If player hits once and stands on 15 ---> player losses (dealer has 18)
        If player hits twice and stands on 18 ---> player draws (dealer has 18)
        If player hits three times and stands on 21 ---> player wins (dealer has 18)

        In this instance the method would store in the matrix:
            results_matrix[12][8]['Hit']['Win'] += 0.333
            results_matrix[12][8]['Hit']['Loss'] += 0.333
            results_matrix[12][8]['Hit']['Draw'] += 0.333

    Example 2:
        player has: 11
        dealer showing: 9 (has a 10 face down)

        The next three cards in the shoe are 2, 6, 10.

        If player hits once and stands on 13 ---> player losses (dealer has 19)
        If player hits twice and stands on 19 ---> player draws (dealer has 19)
        If player hits three times and stands on 29 ---> player losses (dealer has 19)

        In this instance the method would store in the matrix:
            results_matrix[12][8]['Hit']['Win'] += 0.0
            results_matrix[12][8]['Hit']['Loss'] += 0.666
            results_matrix[12][8]['Hit']['Draw'] += 0.333

    Example 3:
        player has: 11
        dealer showing: 9 (has a 10 face down)

        The next three cards in the shoe are 10, 2.

        If player hits once, has 21 ---> player wins (dealer has 19)
        Player only hits once

        In this instance the method would store in the matrix:
            results_matrix[12][8]['Hit']['Win'] += 1.0
            results_matrix[12][8]['Hit']['Loss'] += 0.0
            results_matrix[12][8]['Hit']['Draw'] += 0.0

    """
    working_copy = deepcopy(table)
    dealer_score = get_hand_score(working_copy.dealer.all_cards[0:1])

    for x in range(len(table.players)):

        while not hand_busted(working_copy.players[x].all_cards):
            # Get score for the decision node
            player_score = get_hand_score(working_copy.players[x].all_cards)

            # Deal player a card
            working_copy.players[x].add_card(working_copy.shoe.deal_one())
            print(f"{working_copy.players[x].name} draws {working_copy.players[x].allcards[-1]}")
            print(f"{working_copy.players[x].name} score: {get_hand_score(working_copy.players[x].allcards)} ")

            # Make another deep copy, draw for dealer, evaluate game, and store result
            evaluation_copy = deepcopy(working_copy)
            evaluation_copy.dealer_draws()
            print(dealer_score)


run_game_simulation(1)