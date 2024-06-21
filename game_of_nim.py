from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3, 1]):
        self.initial = GameState(
            to_move='MAX',
            utility=0,
            board=board,
            moves=self.get_moves(board)
        )

    def get_moves(self, board):
        """Generate all possible moves for the current board."""
        moves = []
        for row in range(len(board)):
            for count in range(1, board[row] + 1):
                moves.append((row, count))
        return moves

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        """Return the resulting state after a move."""
        new_board = state.board[:]
        row, count = move
        new_board[row] -= count
        return GameState(
            to_move=('MIN' if state.to_move == 'MAX' else 'MAX'),
            utility=self.compute_utility(new_board, state.to_move),
            board=new_board,
            moves=self.get_moves(new_board)
        )

    def compute_utility(self, board, player):
        """Compute the utility for the current player."""
        if self.terminal_test(GameState(to_move=player, board=board, utility=0, moves=[])):
            return -1 if player == 'MAX' else 1
        return 0

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left."""
        return all(count == 0 for count in state.board)

    def display(self, state):
        """Display the current state of the board."""
        print("board: ", state.board)

if __name__ == "__main__":
    nim = GameOfNim(board=[7, 5, 3, 1]) # Creating the game instance
    # nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [7, 5, 3, 1]
    print(nim.initial.moves) # must be [(0, 1), (0, 2), (0, 3), ..., (3, 1)]

    initial = nim.initial
    print(initial.board == [7, 5, 3, 1])
    print(len(initial.moves) == 16)
    print(nim.terminal_test(initial) == False)
    print(nim.result(initial, (1, 2)).board == [7, 3, 3, 1])
    print(nim.result(initial, (0, 7)).board == [0, 5, 3, 1])

    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
