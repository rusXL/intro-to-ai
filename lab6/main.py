import gymnasium as gym
import numpy as np
from tqdm import tqdm
from typing import Callable, Optional

##############################################

seed = 18
np.random.seed(seed)

##############################################


class QLearner:
    def __init__(
        self,
        #
        state_space: gym.Space,
        action_space: gym.Space,
        #
        learning_rate: float,
        discount: float,
        #
        epsilon: float,
        epsilon_decay_fn: Optional[Callable[[float], float]] = None,
    ):
        """Init a Q-table, Save necessary Params."""
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_decay_fn = epsilon_decay_fn
        self.training_error = []
        self.reset()

    def update(self, state, action: int, reward: float, new_state):
        """Update Value with Temporal Difference Approach."""
        former_q = self.table[state, action]
        future_q = np.max(self.table[new_state, :])

        # Updating Policy: discount * max future Q
        temp_diff_tgt = reward + (self.discount * future_q)
        temp_diff_err = temp_diff_tgt - former_q
        self.training_error.append(temp_diff_err)

        new_q = former_q + self.lr * temp_diff_err

        self.table[state, action] = new_q  # update table
        if self.epsilon_decay_fn is not None:  # decay epsilon
            self.epsilon = self.epsilon_decay_fn(self.epsilon)

    def reset(self):
        """Null the Q-table."""
        self.table = np.zeros((self.state_space.n, self.action_space.n))

    def choose_action(self, state) -> int:
        """Acting Policy: Epsilon-Greedy Strategy."""
        if np.random.random() < self.epsilon:
            action = self.action_space.sample()
        else:
            action = int(np.argmax(self.table[state, :]))
        return action


##############################################
# Set the values for hyperparameters
n_episodes = 50_000
learning_rate = 0.001
discount = 0.95

# Epsilon decay
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = 0.1 

epsilon_decay_fn = lambda epsilon: max(final_epsilon, epsilon - epsilon_decay)


env = gym.make("CliffWalking-v0")
env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)
env.action_space.seed(seed)

agent = QLearner(
    env.observation_space,
    env.action_space,
    learning_rate,
    discount,
    start_epsilon,
    epsilon_decay_fn=epsilon_decay_fn,  # disable decay here
)

# NOTICE:
# If the agent takes an action that would move it off the grid,
# - the environment does not move the agent;
# - applies default reward (-1);
# - returns new_state == state, not an error.

# That is why in Q-table you can see that sometimes agent prefers to move out of the grid.
# Of course this is not optimal, but since the strategy is eps-greedy, it can happen so.

for episode in tqdm(range(n_episodes)):
    state, _ = env.reset(seed=seed)
    done = False

    while not done:
        action = agent.choose_action(state)

        new_state, reward, terminated, truncated, _ = env.step(action)
        agent.update(state, action, reward, new_state)

        done = terminated or truncated
        state = new_state

##############################################

from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme()

def qtable_directions_map(qtable, length, width):
    """Get the best learned action & map it to arrows."""

    qtable_val_max = qtable.max(axis=1).reshape(length, width)
    qtable_best_action = np.argmax(qtable, axis=1).reshape(length, width)
    directions = {0: "↑", 1: "→", 2: "↓", 3: "←"}

    qtable_directions = np.empty(qtable_best_action.flatten().shape, dtype=str)

    for idx, val in enumerate(qtable_best_action.flatten()):
        if qtable_val_max.flatten()[idx] != 0:
            qtable_directions[idx] = directions[val]

    qtable_directions = qtable_directions.reshape(length, width)
    return qtable_val_max, qtable_directions

def plot_q_values_map(qtable, length, width):
    """Plot the last frame of the simulation and the policy learned."""
    qtable_val_max, qtable_directions = qtable_directions_map(qtable, length, width)

    # Plot the last frame
    fig, ax = plt.subplots(figsize=(12, 4))  # 15, 5

    # Plot the policy
    sns.heatmap(
        qtable_val_max,
        annot=qtable_directions,
        fmt="",
        ax=ax,
        cmap=sns.color_palette("Blues", as_cmap=True),
        linewidths=0.7,
        linecolor="black",
        xticklabels=[],
        yticklabels=[],
        annot_kws={"fontsize": "xx-large"},
        mask=qtable_val_max == 0,
    ).set(title="Learned Q-entries\nArrows represent best action")
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(0.7)
        spine.set_color("black")

    fig.savefig("plots/q_table.png", bbox_inches="tight")


plot_q_values_map(agent.table, 4, 12)


##############################################


def get_moving_avgs(arr, window, convolution_mode):
    return (
        np.convolve(np.array(arr).flatten(), np.ones(window), mode=convolution_mode)
        / window
    )


# Smooth over a 500 episode window
rolling_length = 500

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title("Episode rewards")
reward_moving_average = get_moving_avgs(env.return_queue, rolling_length, "valid")
ax.plot(range(len(reward_moving_average)), reward_moving_average)
plt.tight_layout()
plt.savefig("plots/rewards.png")
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title("Episode lengths")
length_moving_average = get_moving_avgs(env.length_queue, rolling_length, "valid")
ax.plot(range(len(length_moving_average)), length_moving_average)
plt.tight_layout()
plt.savefig("plots/lengths.png")
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title("Training Error")
training_error_moving_average = get_moving_avgs(
    agent.training_error, rolling_length, "same"
)
ax.plot(range(len(training_error_moving_average)), training_error_moving_average)
plt.tight_layout()
plt.savefig("plots/errors.png")
plt.close()
