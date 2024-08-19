import traci
import csv
import subprocess, argparse

config_file = "../../sumo/simulation/24h_sim.sumocfg"
log_filepath = "light_info.log"
light_data_filepath = "light_info.csv"
gui = False

sumo_cmd = "sumo" if not gui else "sumo-gui"

if gui:
    result = subprocess.run(["open", "-a", "XQuartz"], capture_output=True, text=True)

    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

sumoCmd = [sumo_cmd, "-c", config_file, "-l", log_filepath]
traci.start(sumoCmd)

traffic_light_ids = traci.trafficlight.getIDList()

print("Traffic Light IDs:", traffic_light_ids)

with open(light_data_filepath, mode='w', newline='') as log_file:
    log_writer = csv.writer(log_file)
    log_writer.writerow(["Traffic Light Id", "Controlled Lanes", "Number of Phases"])

    for tl_id in traffic_light_ids:
        print(f"Traffic Light ID: {tl_id}")

        current_state = traci.trafficlight.getRedYellowGreenState(tl_id)
        print(f"Current State: {current_state}")

        controlled_lanes = len(traci.trafficlight.getControlledLanes(tl_id))
        print(f"Controlled Lanes: {controlled_lanes}")

        num_phases = len(traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0].phases)
        print(f"Number of Phases: {num_phases}")

        log_writer.writerow([tl_id, controlled_lanes, num_phases])

traci.close()

print("Simulation completed and data logged.")