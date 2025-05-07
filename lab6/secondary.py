import gymnasium as gym
import numpy as np
from tqdm import tqdm


##############################################

seed = 18
np.random.seed(seed)

##############################################


class QLearner:
    def __init__(
        self,
        learning_rate: float,
        discount: float,
        epsilon: float,
        state_space: int,
        action_space: int,
    ):
        """Init a Q-table, Save necessary Params."""
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.discount = discount
        self.epsilon = epsilon
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

        new_q = self.table[state, action] + self.lr * temp_diff_err
        return new_q

    def reset(self):
        """Null the Q-table."""
        self.table = np.zeros((self.state_space.n, self.action_space.n))

    def choose_action(self, state):
        """Acting Policy: Epsilon-Greedy Strategy."""
        if np.random.random() < self.epsilon:
            action = self.action_space.sample()
        else:
            action = int(np.argmax(self.table[state, :]))
        return action


##############################################

n_episodes = 1000
learning_rate = 0.01
epsilon = 0.75
discount = 0.95

env = gym.make("CliffWalking-v0")
env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)

agent = QLearner(
    learning_rate, discount, epsilon, env.observation_space, env.action_space
)


for episode in tqdm(range(n_episodes)):
    state, _ = env.reset()
    done = False

    while not done:
        action = agent.choose_action(state)

        new_state, reward, terminated, truncated, _ = env.step(action)
        agent.update(state, action, reward, new_state)

        done = terminated or truncated
        state = new_state


##############################################

from matplotlib import pyplot as plt


def get_moving_avgs(arr, window, convolution_mode):
    return (
        np.convolve(np.array(arr).flatten(), np.ones(window), mode=convolution_mode)
        / window
    )


# Smooth over a 500 episode window
rolling_length = 500
fig, axs = plt.subplots(ncols=3, figsize=(12, 5))

axs[0].set_title("Episode rewards")
reward_moving_average = get_moving_avgs(env.return_queue, rolling_length, "valid")
axs[0].plot(range(len(reward_moving_average)), reward_moving_average)

axs[1].set_title("Episode lengths")
length_moving_average = get_moving_avgs(env.length_queue, rolling_length, "valid")
axs[1].plot(range(len(length_moving_average)), length_moving_average)

axs[2].set_title("Training Error")
training_error_moving_average = get_moving_avgs(
    agent.training_error, rolling_length, "same"
)
axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)


plt.tight_layout()
plt.show()
plt.savefig("plot.png")
