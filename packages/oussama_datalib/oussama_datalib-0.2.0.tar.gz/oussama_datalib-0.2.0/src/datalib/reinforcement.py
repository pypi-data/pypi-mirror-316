"""
Functions for reinforcement learning algorithms.
"""
import numpy as np

def basic_q_learning(environment, episodes, alpha, gamma, epsilon=0.1):
    """
    Implement the Q-learning algorithm.

    Args:
        environment: The RL environment.
        episodes: Number of episodes to train.
        alpha: Learning rate.
        gamma: Discount factor.
        epsilon: Exploration rate.
    """
    q_table = np.zeros((environment.observation_space.n, environment.action_space.n))
    for episode in range(episodes):
        state = environment.reset()
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = environment.action_space.sample()
            else:
                action = np.argmax(q_table[state])
            next_state, reward, done, _ = environment.step(action)
            q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state, action])
            state = next_state
    return q_table

def sarsa(environment, episodes, alpha, gamma, epsilon=0.1):
    """
    Implement the SARSA algorithm.

    Args:
        environment: The RL environment.
        episodes: Number of episodes to train.
        alpha: Learning rate.
        gamma: Discount factor.
        epsilon: Exploration rate.
    """
    q_table = np.zeros((environment.observation_space.n, environment.action_space.n))
    for episode in range(episodes):
        state = environment.reset()
        action = environment.action_space.sample() if np.random.rand() < epsilon else np.argmax(q_table[state])
        done = False
        while not done:
            next_state, reward, done, _ = environment.step(action)
            next_action = environment.action_space.sample() if np.random.rand() < epsilon else np.argmax(q_table[next_state])
            q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * q_table[next_state, next_action] - q_table[state, action])
            state, action = next_state, next_action
    return q_table
