import os
import numpy as np
import traci
import subprocess


class TrafficSignalControl:
    def __init__(self, sim_name, config_filepath, output_dir='', gui=False):
        self.sim_name = sim_name
        self.config_filepath = config_filepath
        self.gui = gui
        self.output_dir = os.path.join(output_dir, sim_name)
        self.log_filepath = os.path.join(self.output_dir, "sim_log.log")
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)
        self.sumo_cmd = "sumo" if not gui else "sumo-gui"
        self.simulation_running = False
        self.traci = traci

    def _start_xquartz(self):
        result = subprocess.run(["open", "-a", "XQuartz"], capture_output=True, text=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

    def start_simulation(self):
        if self.gui:
            self._start_xquartz()

        sumoCmd = [self.sumo_cmd, "-c", self.config_filepath, "-l", self.log_filepath]
        print("SUMO Command:", sumoCmd)
        self.traci.start(sumoCmd)
        self.simulation_running = True

    def step(self):
        if not self.simulation_running:
            raise RuntimeError("Simulation has not been started. Call start_simulation() first.")

        if self.traci.simulation.getMinExpectedNumber() > 0:
            self.traci.simulationStep()
        else:
            self.simulation_running = False
            print("All routes have been parsed completey")

    def close_simulation(self):
        if self.simulation_running:
            self.traci.close()
            self.simulation_running = False
            print("Simulation completed and data logged.")
        else:
            print("Simulation was not running.")

    def get_traffic_light_observations(self, tl_id):
        observation = []

        # Current Traffic Light State
        current_phase = self.traci.trafficlight.getRedYellowGreenState(tl_id)
        time_since_last_change = self.traci.trafficlight.getPhaseDuration(tl_id)
        observation.append(current_phase)
        observation.append(time_since_last_change)

        # Traffic Density (for each controlled lane)
        controlled_lanes = self.traci.trafficlight.getControlledLanes(tl_id)
        for lane_id in controlled_lanes:
            num_vehicles = self.traci.lane.getLastStepVehicleNumber(lane_id)
            queue_length = self.traci.lane.getLastStepHaltingNumber(lane_id)
            avg_speed = self.traci.lane.getLastStepMeanSpeed(lane_id)
            observation.extend([num_vehicles, queue_length, avg_speed])

        # Traffic Flow Information (for each controlled lane)
        for lane_id in controlled_lanes:
            arrival_rate = self.traci.lane.getLastStepVehicleNumber(lane_id)  # Approximation for arrival rate
            time_gaps = self.traci.lane.getLastStepVehicleHaltingNumber(lane_id)  # Not exact but indicative
            observation.extend([arrival_rate, time_gaps])

        # Vehicle Types (for each controlled lane)
        for lane_id in controlled_lanes:
            vehicle_types = self.traci.lane.getLastStepVehicleIDs(lane_id)
            car_count = sum(1 for veh_id in vehicle_types if self.traci.vehicle.getVehicleClass(veh_id) == 'passenger')
            bus_count = sum(1 for veh_id in vehicle_types if self.traci.vehicle.getVehicleClass(veh_id) == 'bus')
            truck_count = sum(1 for veh_id in vehicle_types if self.traci.vehicle.getVehicleClass(veh_id) == 'truck')
            observation.extend([car_count, bus_count, truck_count])

        # Pedestrian Information (for each crosswalk linked to the traffic light)
        pedestrian_crossings = self.traci.trafficlight.getControlledLinks(
            tl_id)  # This gives lane links, adjust for crosswalks
        for link in pedestrian_crossings:
            pedestrian_lane = link[0][0]  # Assuming first element is the pedestrian lane
            pedestrian_waiting_time = self.traci.lane.getWaitingTime(pedestrian_lane)
            pedestrian_count = self.traci.lane.getLastStepPersonNumber(pedestrian_lane)
            observation.extend([pedestrian_waiting_time, pedestrian_count])

        # Intersection Characteristics (assuming fixed for this example, can be adjusted based on the layout)
        num_lanes = len(controlled_lanes)
        observation.append(num_lanes)

        # Phase Switching History (simplified, last phase duration and phase state)
        previous_phase = self.traci.trafficlight.getPhase(tl_id)
        observation.append(previous_phase)

        # Convert observation list to numpy array for easy processing in RL algorithms
        observation_vector = np.array(observation)

        return observation_vector


sim_name = 'network_info/2023-06-19'
config_filepath = "/users/pdm523/sumo_ingolstadt_marl/src/environment/simulations/Ingolstadt SUMO 365/2023-06-19.sumocfg"

simulation = TrafficSignalControl(sim_name, config_filepath)
simulation.start_simulation()