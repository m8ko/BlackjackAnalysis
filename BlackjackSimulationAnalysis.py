from Player import Player
from BlackjackTable import BlackjackTable, get_hand_score, hand_busted
from pprint import pprint
from copy import deepcopy

results_matrix = [
    [{"Hit": {'Win': 0, 'Loss': 0, 'Draw': 0}, "Stand": {'Win': 0, 'Loss': 0, 'Draw': 0}} for i in range(11)] for y in
    range(21)]

sim_table = BlackjackTable([Player('Player1')])
sim_table.shoe.shuffle()


def get_stand_probability():
    for x in range(10000000):
        needs_reset = len(sim_table.shoe.all_cards) < sim_table.cut_card_position

        # for player in sim_table.players:
        #     print(player)

        # Checks if the shoe has has come across cut card and resets if so
        if needs_reset:
            sim_table.reset_shoe()

        # print(sim_table.shoe)
        # print(f"The dc pile has {len(sim_table.discard_pile)}")

        sim_table.deal_cards(False)
        simulate_stand(sim_table)
        sim_table.clear_table_cards()


def simulate_stand(table):
    """
    Accepts a Simulates a player standing on hand using table object and adds the result to the matrix
    """

    # for player in table.players:
    #     print(f"{player.name} stands with a {get_hand_score(player.all_cards)}")

    table.dealer_draws(print_action=False)

    # Get score of dealer's up card and list of player scores
    dealer_score = get_hand_score(table.dealer.all_cards[0:1])
    # print(dealer_score)
    player_scores = [get_hand_score(table.players[x].all_cards) for x in range(len(table.players))]
    player_results = table.evaluate_game()

    player_result_tuples = list(zip(player_scores, ['Stand' for y in range(len(player_scores))], player_results))

    # print(player_result_tuples)

    store_results(dealer_score, player_result_tuples)


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


def print_results_matrix():
    print(' ,1,2,3,4,5,6,7,8,9,10,11')

    for x in range(len(results_matrix)):
        row_results = [x+1]
        for y in range(len(results_matrix[x])):
            stand = results_matrix[x][y]['Stand']
            win = stand['Win']
            loss = stand['Loss']
            draw = stand['Draw']
            observations = (win + loss + draw)
            if observations==0:
                row_results.append('')
            else:
                win_percentage = win/observations
                loss_percentage = loss/observations
                payout_to_stand = win_percentage*1 + loss_percentage*-1
                row_results.append(payout_to_stand)

        for i in range(len(row_results)):
            print(row_results[i], end=",")

        print()

get_stand_probability()
print_results_matrix()
