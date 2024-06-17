from games import Game, GameState
import sys

class GameOfNim(Game):
    def __init__(self, initial_board):
        self.initial = GameState(to_move='MAX', utility=0, board=initial_board, moves=self.get_moves(initial_board))

    def get_moves(self, board):
        moves = []
        for r, num_objects in enumerate(board):
            for n in range(1, num_objects + 1):
                moves.append((r, n))
        return moves

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        board = state.board[:]
        r, n = move
        board[r] -= n
        moves = self.get_moves(board)
        return GameState(
            to_move=('MIN' if state.to_move == 'MAX' else 'MAX'),
            utility=self.compute_utility(board, state.to_move),
            board=board,
            moves=moves
        )

    def compute_utility(self, board, player):
        if all(x == 0 for x in board):
            return -1 if player == 'MAX' else 1
        return 0

    def terminal_test(self, state):
        return all(x == 0 for x in state.board)

    def utility(self, state, player):
        return state.utility

    def display(self, state):
        print(f"board: {state.board}")

def query_player(game, state):
    print(f"current state: board: {state.board}")
    print(f"available moves: {state.moves}")

    while True:
        try:
            move = input("\nYour move? ")
            move = eval(move)  # Safely evaluate user input
            if move in state.moves:
                return move
            else:
                print("Invalid move. Please try again.")
        except (NameError, SyntaxError):
            print("Invalid input format. Please enter (row, number).")

def minmax_decision(state, game):
    player = game.to_move(state)
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player), None

        value = -sys.maxsize
        best_move = None
        for action in game.actions(state):
            result_state = game.result(state, action)
            min_val, _ = min_value(result_state, alpha, beta)
            if min_val > value:
                value = min_val
                best_move = action
            if value >= beta:
                return value, best_move
            alpha = max(alpha, value)
        return value, best_move

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player), None

        value = sys.maxsize
        best_move = None
        for action in game.actions(state):
            result_state = game.result(state, action)
            max_val, _ = max_value(result_state, alpha, beta)
            if max_val < value:
                value = max_val
                best_move = action
            if value <= alpha:
                return value, best_move
            beta = min(beta, value)
        return value, best_move

    return max_value(state, -sys.maxsize, sys.maxsize)[1]

def play_game(game, query_player, minmax_player):
    state = game.initial
    while not game.terminal_test(state):
        game.display(state)
        if game.to_move(state) == 'MAX':
            move = minmax_player(state, game)
            print(f"Computer plays: {move}")
        else:
            move = query_player(game, state)
        state = game.result(state, move)
    game.display(state)
    if game.utility(state, 'MAX') == 1:
        print("MAX won the game")
    else:
        print("MIN won the game")

if __name__ == '__main__':
    initial_board = [7, 5, 3, 1]
    game = GameOfNim(initial_board)
    play_game(game, query_player, minmax_decision)
