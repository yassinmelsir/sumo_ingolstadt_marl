import torch
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

from src.algorithms.qmix.mixing_network import MixingNetwork
from src.algorithms.qmix.q_network import QNetwork
from src.algorithms.qmix.replay_buffer import ReplayBuffer


class QMIX:
    def __init__(self, n_agents, state_dim, obs_dim, n_actions, buffer_size, batch_size, gamma, lr):
        self.n_agents = n_agents
        self.state_dim = state_dim
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.gamma = gamma
        self.batch_size = batch_size

        self.q_networks = [QNetwork(obs_dim, n_actions) for _ in range(n_agents)]
        self.mixing_network = MixingNetwork(n_agents, state_dim)
        self.target_mixing_network = MixingNetwork(n_agents, state_dim)

        self.optimizers = [optim.Adam(q.parameters(), lr=lr) for q in self.q_networks]
        self.mixing_optimizer = optim.Adam(self.mixing_network.parameters(), lr=lr)

        self.replay_buffer = ReplayBuffer(buffer_size, batch_size)

    def select_action(self, obs, epsilon):
        actions = []
        for i, q_net in enumerate(self.q_networks):
            if np.random.rand() < epsilon:
                actions.append(np.random.randint(self.n_actions))
            else:
                q_values = q_net(torch.tensor(obs[i], dtype=torch.float32))
                actions.append(torch.argmax(q_values).item())
        return actions

    def add_experience(self, obs, actions, rewards, next_obs, done):
        self.replay_buffer.add((obs, actions, rewards, next_obs, done))

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        batch = self.replay_buffer.sample()
        obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = zip(*batch)

        obs_batch = np.array(obs_batch)
        action_batch = np.array(action_batch)
        reward_batch = np.array(reward_batch)
        next_obs_batch = np.array(next_obs_batch)
        done_batch = np.array(done_batch)

        q_values = []
        next_q_values = []

        for i in range(self.n_agents):
            q_values.append(self.q_networks[i](torch.tensor(obs_batch[:, i], dtype=torch.float32)))
            next_q_values.append(self.q_networks[i](torch.tensor(next_obs_batch[:, i], dtype=torch.float32)))

        q_values = torch.stack(q_values, dim=1)
        next_q_values = torch.stack(next_q_values, dim=1)

        chosen_q_values = torch.gather(q_values, dim=-1, index=torch.tensor(action_batch[..., None]).long()).squeeze(-1)
        target_q_values = torch.max(next_q_values, dim=-1)[0]

        with torch.no_grad():
            target_values = torch.tensor(reward_batch, dtype=torch.float32) + self.gamma * target_q_values * (
                        1 - torch.tensor(done_batch, dtype=torch.float32))

        loss = F.mse_loss(chosen_q_values, target_values)

        for optimizer in self.optimizers:
            optimizer.zero_grad()
        loss.backward()
        for optimizer in self.optimizers:
            optimizer.step()

        state_batch = torch.tensor(obs_batch.mean(axis=1), dtype=torch.float32)
        mixed_q_values = self.mixing_network(state_batch, chosen_q_values)
        target_mixed_q_values = self.target_mixing_network(state_batch, target_q_values)

        mixing_loss = F.mse_loss(mixed_q_values, target_mixed_q_values)

        self.mixing_optimizer.zero_grad()
        mixing_loss.backward()
        self.mixing_optimizer.step()

    def update_target_network(self):
        self.target_mixing_network.load_state_dict(self.mixing_network.state_dict())