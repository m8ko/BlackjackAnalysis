from Player import Player
from BlackjackTable import BlackjackTable, get_hand_score
from time import perf_counter
import functools

results_matrix = [
    [{"Hit": {'Win': 0, 'Loss': 0, 'Draw': 0}, "Stand": {'Win': 0, 'Loss': 0, 'Draw': 0}} for i in range(11)] for y in
    range(21)]

sim_table = BlackjackTable([Player('Player1')])
sim_table.shoe.shuffle()


def time_efficiency(func):
    # Decorator that allows one to test how long it takes for a function to execute and prints to console

    @functools.wraps(func)
    def wrap_func(*args, **kwargs):
        start = perf_counter()
        func(*args, **kwargs)
        print(f"Time to execute: {perf_counter() - start}")

    return wrap_func


@time_efficiency
def get_stand_probability(num_of_rounds):
    for x in range(num_of_rounds):
        needs_reset = len(sim_table.shoe.all_cards) < sim_table.cut_card_position

        if needs_reset:  # Checks if the shoe has has come across cut card and resets if so
            sim_table.reset_shoe()

        sim_table.deal_cards(False)  # Deals cards to players and dealer, doesn't print deal
        simulate_stand(sim_table)
        sim_table.clear_table_cards()  # Move cards to discard pile


def simulate_stand(table):
    """
    Accepts a Simulates a player standing on hand using table object and adds the result to the matrix
    """

    table.dealer_draws(print_action=False)

    # Get score of dealer's up card and list of player scores
    dealer_score = get_hand_score(table.dealer.all_cards[0:1])
    player_scores = [get_hand_score(table.players[x].all_cards) for x in range(len(table.players))]

    player_results = table.evaluate_game()

    player_result_tuples = list(zip(player_scores, ['Stand' for y in range(len(player_scores))], player_results))

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

        if result or result == 'Blackjack':  # player wins or blackjack
            results_matrix[player_score - 1][dlr_score - 1][action]['Win'] += 1

        elif not result:  # player loses
            results_matrix[player_score - 1][dlr_score - 1][action]['Loss'] += 1

        else:  # Draws with dealer
            results_matrix[player_score - 1][dlr_score - 1][action]['Draw'] += 1


def write_list_to_csv(file_object, lst):
    list_as_string = str(lst)[1:-1].replace(" ''", '')
    file_object.write(list_as_string)
    file_object.write('\n')

def print_results_to_csv():
    """
    Prints the results matrix in a manner that can be easily imported to a csv file. The number that is printed out
    for the matrix is a number between -1 and 1 which is essentially a payout multiple.
    """

    results = open('exp_payout_to_stand.csv', 'w+')
    results.write(',2,3,4,5,6,7,8,9,10,11\n')

    observations_file = open('observations.csv', 'w+')
    observations_file.write(',2,3,4,5,6,7,8,9,10,11\n')

    for row_index in range(3, len(results_matrix)):
        row_results = [row_index + 1]  # Holds the result for a row. First element is the row index + 1 (player's score)
        observations = [row_index + 1]

        # Retrieves values from matrix and calculates payout to stand based on player score and dealer show card
        for column_index in range(1, len(results_matrix[row_index])):
            stand = results_matrix[row_index][column_index]['Stand']

            win, loss, draw = stand['Win'], stand['Loss'], stand['Draw']

            obs = sum([win, loss, draw])
            observations.append(obs)

            if obs == 0:  # Avoids a divide by zero error
                row_results.append('')
            else:  #
                win_percentage = win / obs
                loss_percentage = loss / obs
                exp_payout_to_stand = win_percentage * 1 + loss_percentage * -1
                row_results.append(exp_payout_to_stand)

        write_list_to_csv(results, row_results)
        write_list_to_csv(observations_file, observations)

    results.close()
    observations_file.close()

get_stand_probability(10000000)
print_results_to_csv()
