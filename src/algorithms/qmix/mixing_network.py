import torch
from torch import nn


class MixingNetwork(nn.Module):
    def __init__(self, n_agents, state_dim):
        super(MixingNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, n_agents)

    def forward(self, state, agent_qs):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return torch.sum(self.fc3(x) * agent_qs, dim=-1)