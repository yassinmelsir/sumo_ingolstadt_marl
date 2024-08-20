import traci
import torch
import numpy as np
from algorithms.qmix.qmix import QMIX


def get_observations():
    obs = []
    for tl in traci.trafficlight.getIDList():
        obs.append(get_state_for_traffic_light(tl))
    return obs


def get_state_for_traffic_light(tl_id):
    lanes = traci.trafficlight.getControlledLanes(tl_id)
    state = []
    for lane in lanes:
        state.append(traci.lane.getLastStepVehicleNumber(lane))
    return np.array(state)

def get_rewards():
    rewards = []
    for tl in traci.trafficlight.getIDList():
        for lane in traci.trafficlight.getControlledLanes(tl):
            rewards.append(traci.lane.getLastStepMeanSpeed(lane))

    return rewards


def main():
    sumoBinary = "sumo"
    sumoCmd = [sumoBinary, "-c", "sumo_network/your_sumo_config.sumocfg"]

    traci.start(sumoCmd)

    n_agents = len(traci.trafficlight.getIDList())
    state_dim = len(get_observations()[0])
    obs_dim = state_dim
    n_actions = 3  # Example: 3 actions - stay, switch phase, extend current phase

    qmix = QMIX(n_agents, state_dim, obs_dim, n_actions, buffer_size=5000, batch_size=32, gamma=0.99, lr=0.001)

    epsilon = 1.0
    decay = 0.995
    min_epsilon = 0.1

    for episode in range(1000):
        traci.load(sumoCmd)
        total_reward = 0

        while traci.simulation.getMinExpectedNumber() > 0:
            obs = get_observations()
            actions = qmix.select_action(obs, epsilon)

            for i, tl in enumerate(traci.trafficlight.getIDList()):
                if actions[i] == 0:  # stay
                    pass
                elif actions[i] == 1:  # switch phase
                    traci.trafficlight.setPhase(tl, (traci.trafficlight.getPhase(tl) + 1) % 4)
                elif actions[i] == 2:  # extend current phase
                    traci.trafficlight.setPhaseDuration(tl, traci.trafficlight.getPhaseDuration(tl) + 5)

            traci.simulationStep()

            next_obs = get_observations()
            rewards = get_rewards()
            done = traci.simulation.getMinExpectedNumber() == 0
            qmix.add_experience(obs, actions, rewards, next_obs, done)
            qmix.update()
            total_reward += sum(rewards)

        qmix.update()

main()