import copy
from typing import TypeAlias

Board: TypeAlias = list[int]
State: TypeAlias = tuple[Board, int]
Action: TypeAlias = tuple[int, int]


def actions(state: State) -> list[Action]:
    """Legal moves for a state."""
    board, _ = state
    moves = []
    for i, sticks in enumerate(board):
        for j in range(1, sticks + 1):
            moves.append((i, j))
    return moves


def result(state: State, action: Action) -> State:
    """Transition model. What is the result state of taking action from state."""
    pile, sticks = action

    new_board, new_turn = copy.deepcopy(state)
    new_board[pile] -= sticks
    new_turn += 1

    return new_board, new_turn


def terminal(state: State) -> bool:
    """Terminal test. Determines when the game is over."""
    board, _ = state
    return sum(board) <= 1


def utility(state: State) -> int:
    """Final numerical value for the terminal state.

    Returns:
        -1: if the User won
        +1: if the AI won
    """
    board, turn = state  # Unpack the state

    # if one is left with 1 stick, it loses
    # if one is left with 0 sticks, one wins
    if turn % 2 == 0:  # AI's turn
        return -1 if sum(board) == 1 else 1
    else:  # User's turn
        return 1 if sum(board) == 1 else -1


def max_move(state: State, alpha: float, beta: float) -> tuple[Action, int]:
    if terminal(state):
        return None, utility(state)

    action = None
    value = float("-inf")

    for a in actions(state):
        _, v = min_move(result(state, a), alpha, beta)

        if v > value:
            action = a
            value = v

        # pruning
        if value >= beta:
            break
        alpha = max(alpha, value)

    return action, value


def min_move(state: State, alpha: float, beta: float) -> tuple[Action, int]:
    if terminal(state):
        return None, utility(state)

    action = None
    value = float("inf")

    for a in actions(state):
        _, v = max_move(result(state, a), alpha, beta)

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

if __name__ == "__main__":
    piles = []
    print("Starting Nim!")

    num_piles = int(input("Input the number of piles: "))

    print("Input the number of sticks in each pile (separate with ENTER)")
    for _ in range(num_piles):
        piles.append(int(input()))

    state = (piles, 1)  # initial state
    print("The person who removes the last stick loses!")
    print("Example: to remove 3 sticks from pile 2, enter: 2 3")

    while not terminal(state):
        board, turn = state  # Get current board & turn

        print("Current Pile State:", board)

        if turn % 2 == 0:  # AI's Turn
            print("AI's turn ")
            action, _ = max_move(state, float("-inf"), float("inf"))

            print(f"AI removes {action[1]} stick(s) from pile {action[0]}")
        else:  # User's Turn
            while True:
                try:
                    action = tuple(
                        map(
                            int,
                            input("Your move (pile index sticks to remove): ").split(),
                        )
                    )
                    if action in actions(state):
                        break
                    print("Invalid move! Try again.")
                except ValueError:
                    print("Invalid input! Enter two numbers.")

        state = result(state, action)  # Apply move

    # Game Over Message
    print("\nFinal Pile State:", state[0])
    if utility(state) == 1:
        print("\nAI Wins! Better luck next time. 🤖🏆")
    else:
        print("\nYou Win! Congratulations! 🎉")
