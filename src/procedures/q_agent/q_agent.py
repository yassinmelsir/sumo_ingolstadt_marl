import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from src.algorithms.q_agent.q_network import QNetwork
from src.sumo.sumo_simulation.sumo_simulation import SumoSimulation


def select_action(state, epsilon):
    if np.random.rand() < epsilon:
        # Random action (exploration)
        return np.random.randint(output_dim)
    else:
        # Greedy action (exploitation)
        with torch.no_grad():
            return q_network(state).argmax().item()

def optimize_model(state, action, reward, next_state, done, gamma=0.99):
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    action = torch.tensor([[action]], dtype=torch.long)
    reward = torch.tensor([reward], dtype=torch.float32)
    done = torch.tensor([done], dtype=torch.float32)

    # Compute Q(s, a)
    q_value = q_network(state).gather(1, action)

    # Compute max Q(s', a')
    with torch.no_grad():
        max_next_q_value = q_network(next_state).max(1)[0].unsqueeze(1)

    # Compute the target Q-value
    expected_q_value = reward + (1.0 - done) * gamma * max_next_q_value

    # Compute the loss
    loss = criterion(q_value, expected_q_value)

    # Optimize the Q-network
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

sim_name = '2023-06-19'
config_filepath = "../../../sumo/simulations/config/2023-06-19.sumocfg"
gui = False

num_episodes = 1000
epsilon_start = 1.0
epsilon_end = 0.01
epsilon_decay = 0.995
gamma = 0.99


simulation = SumoSimulation(sim_name, config_filepath, gui)
simulation.start_simulation()

traffic_light_ids = simulation.traci.vehicle.getIDList()
agent_id = traffic_light_ids[0]

obs = simulation.get_traffic_light_observations(agent_id)
input_dm = len(obs)

q_network = QNetwork(input_dim, output_dim, hidden_dim)
optimizer = optim.Adam(q_network.parameters(), lr=0.001)
criterion = nn.MSELoss()

episode = 0
while simulation.simulation_running and episode <= num_episodes:
    simulation.step()

    simulation_time = simulation.traci.simulation.getTime()


    state = get_initial_state_from_sumo()
    epsilon = max(epsilon_end, epsilon_start * (epsilon_decay ** episode))

    done = False
    while not done:
        action = select_action(state, epsilon)
        next_state, reward, done = step_sumo_simulation(action)

        optimize_model(state, action, reward, next_state, done, gamma)

        state = next_state

    print(f"Episode {episode} completed.")
    episode += 1