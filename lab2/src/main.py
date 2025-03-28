import copy
from typing import TypeAlias

Board: TypeAlias = list[int]
State: TypeAlias = tuple[Board, int]
Action: TypeAlias = tuple[int, int]


def actions(state: State) -> list[Action]:
    """Legal moves for a `state`."""
    board, _ = state
    moves = []
    for i, sticks in enumerate(board):
        for j in range(1, sticks + 1):
            moves.append((i, j))
    return moves


def result(state: State, action: Action) -> State:
    """Transition model. What is the result state of taking `action` from `state`."""
    pile, sticks = action

    new_board, new_turn = copy.deepcopy(state)
    new_board[pile] -= sticks
    new_turn += 1

    return new_board, new_turn


def terminal(state: State) -> bool:
    """Decides whether the `state` is terminal. Determines when the game is over."""
    board, _ = state
    return sum(board) <= 1


def utility(state: State) -> int:
    """Final numerical value for the terminal `state`.
    -1: if User wins.
    +1: if AI wins.
    """
    board, turn = state

    # if one is left with 1 stick, it loses
    # if one is left with 0 sticks, it wins
    if turn % 2 == 0:  # AI's turn
        return -1 if sum(board) == 1 else 1
    else:  # User's turn
        return 1 if sum(board) == 1 else -1


def evaluate(state: State) -> int:
    """Estimates expected utility of the game from the `state`. Heuristic evaluation based on Nim-Sum."""
    board, turn = state
    nim_sum = 0

    for pile in board:
        nim_sum ^= pile

    if turn % 2 == 0:  # AI's turn
        return -1 if nim_sum == 0 else 1
    else:  # User's turn
        return 1 if nim_sum == 0 else -1


def max_move(state: State, alpha: float, beta: float, depth: int) -> tuple[Action, int]:
    """Behaviour of a player trying to maximize the score."""
    if terminal(state):
        # return if reached the terminal state
        return None, utility(state)
    if depth == 0:
        # return if reached the depth
        return None, evaluate(state)

    action = None  # best action
    value = float("-inf")  # highest value

    for a in actions(state):
        # find action `a` that produces the highest value
        # of what min player can achieve if action is taken
        _, v = min_move(result(state, a), alpha, beta, depth - 1)

        if v > value:
            action = a
            value = v

        # pruning
        if value >= beta:
            break
        alpha = max(alpha, value)

    return action, value


def min_move(state: State, alpha: float, beta: float, depth: int) -> tuple[Action, int]:
    """Behaviour of a player trying to minimize the score."""
    if terminal(state):
        # return if reached the terminal state
        return None, utility(state)
    if depth == 0:
        # return if reached the depth
        return None, evaluate(state)

    action = None  # best action
    value = float("inf")  # lowest value

    for a in actions(state):
        # find action `a` that produces the lowest value
        # of what max player can achieve if action is taken
        _, v = max_move(result(state, a), alpha, beta, depth - 1)

        if v < value:
            action = a
            value = v

        # pruning
        if value <= alpha:
            break
        beta = min(beta, value)

    return action, value


# AI - max player: aims to maximize utility of the state
# User - min player: aims to minimize utility of the state


# TODO: you are encouraged to refactor ⬇️⬇️⬇️
# you can add better visualisation for the board
# or improve input handling


def init_game() -> State:
    """Instructions to start the game."""
    board = []

    num_piles = int(input("Input the number of piles: "))

    print("Input the number of sticks in each pile (separate with ENTER)")
    for _ in range(num_piles):
        board.append(int(input()))

    print("Example Action: to remove 3 sticks from pile 2, enter: 2 3")

    return (board, 1)  # initial state (board, turn)


def end_game(state: State):
    print(f"Board: {state[0]}")

    if utility(state) == 1:
        print("AI Wins! 🤖🏆")
    else:
        print("You Win! 👻🎉")


if __name__ == "__main__":
    DEPTH = 5
    state = init_game()

    while not terminal(state):
        board, turn = state

        print(f"Board: {board}")

        if turn % 2 == 0:  # AI's Turn
            action, _ = max_move(state, float("-inf"), float("inf"), DEPTH)
            print(f"AI removes {action[1]} stick(s) from pile {action[0]}")
        else:  # User's Turn
            while True:
                try:
                    action = tuple(
                        map(
                            int,
                            input("Your move: ").split(),
                        )
                    )
                    if action in actions(state):
                        break
                    print("Try again")
                except ValueError:
                    print("Try again")

        state = result(state, action)  # transition

    end_game(state)

    # Game Over Message
