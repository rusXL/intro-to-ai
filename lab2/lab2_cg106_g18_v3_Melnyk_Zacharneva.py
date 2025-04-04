import copy
from typing import TypeAlias
from enum import Enum
from typing import NamedTuple

Board: TypeAlias = list[int]

class State(NamedTuple):
    board: Board
    turn: int

class Action(NamedTuple):
  pile: int
  sticks: int

class Player(Enum):
    AI = 1
    USER = -1


def get_player(state: State) -> Player:
    """Which player is to move at `state`."""
    return Player.AI if state.turn % 2 == 0 else Player.USER

def get_result(state: State, action: Action) -> State:
    """Transition model. What is the result state of taking `action` from `state`."""
    new_board, new_turn = copy.deepcopy(state)
    new_board[action.pile] -= action.sticks
    new_turn += 1
    return State(new_board, new_turn)


def is_terminal(state: State) -> bool:
    """Decides whether the `state` is terminal. Determines when the game is over."""
    return sum(state.board) <= 1


def evaluate(state: State) -> int:
    """Estimates expected utility of the game from the `state`. Heuristic evaluation based on Nim-Sum.
    If the state is terminal, return final numerical value: -1 if User wins and +1 if AI wins.
    """
    nim_sum = 0
    for pile in state.board:
        nim_sum ^= pile

    lose = (sum(state.board) == 1) or (nim_sum == 0)

    if (get_player(state) == Player.AI and lose) or (get_player(state) == Player.USER and not lose):
      return Player.USER.value
    else:
      return Player.AI.value


def minimax(state: State, alpha: float, beta: float, depth: int, is_max: bool) -> tuple[Action, int]:
    if is_terminal(state) or depth == 0:
        return None, evaluate(state)

    action = None  # best action
    value = float("-inf") if is_max else float("inf")

    current_node_id = graph.node_id

    for i, sticks in enumerate(state.board):
        for j in range(1, sticks + 1):
          a = Action(i, j)
          if (sum(get_result(state, a).board)) == 0:
            continue
          _, v = minimax(get_result(state, a), alpha, beta, depth - 1, (not is_max))
          # Maximizing player
          if is_max:
            if v > value:
              value = v
              action = a
            if value >= beta:
              break
            alpha = max(alpha, value)
          # Minimizing player
          else:
            if v < value:
              value = v
              action = a
            if value <= alpha:
              break
            beta = min(beta, value)
    return action, value


# AI - max player: aims to maximize utility of the state
# User - min player: aims to minimize utility of the state


def print_board(board):
    """Visualize the board with stick emojis."""
    print(board)


def init_game() -> State:
    """Instructions to start the game."""
    board = []
    while True:
      try:
        num_piles = int(input("Input the number of piles: "))
        break
      except ValueError:
        print("Try again.")


    print("Input the number of sticks in each pile (separate with ENTER).")
    while True and num_piles > 0:
      try:
        board.append(int(input()))
        num_piles -= 1
      except ValueError:
        print("Try again. Please separate numbers with ENTER.")


    print("Example Action: to remove 3 sticks from pile 2, enter: 2 3. Piles are counted from 0.")

    return State(board, 1)  # initial state (board, turn); user always starts first


def end_game(state: State):
    print_board(state.board)

    if evaluate(state) == 1:
        print("AI Wins! 🤖🏆")
    else:
        print("You Win! 👻🎉")


if __name__ == "__main__":
    state = init_game()
    DEPTH = 5
    while not is_terminal(state):
        print_board(state.board)

        match get_player(state):
            case Player.AI:
                action, _ = minimax(state, float("-inf"), float("inf"), DEPTH, True)
                print(f"AI removes {action.sticks} stick(s) from pile {action.pile}")

            case Player.USER:
                while True:
                    try:
                        pile, sticks = input("Your move: ").split()
                        action = Action(int(pile), int(sticks))
                        if len(state.board) > action.pile and state.board[action.pile] >= action.sticks:
                            break
                        print("Try again")
                    except ValueError:
                        print("Try again")

        state = get_result(state, action)  # transition

    end_game(state)
