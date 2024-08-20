import os

import traci
import csv
import subprocess

sim_name = '2023-06-19'
config_filepath = "../../sumo/simulation/Ingolstadt SUMO 365/2023-06-19.sumocfg"
gui = False

output_dir = os.path.join(".", sim_name)

log_filepath = os.path.join(output_dir, "sim_log.log")
network_data_filepath = os.path.join(output_dir, "vehicle_data.csv")
light_data_filepath = os.path.join(output_dir, "light_info.csv")

os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
os.makedirs(os.path.dirname(light_data_filepath), exist_ok=True)
os.makedirs(os.path.dirname(network_data_filepath), exist_ok=True)

sumo_cmd = "sumo" if not gui else "sumo-gui"

if gui:
    result = subprocess.run(["open", "-a", "XQuartz"], capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


sumoCmd = [sumo_cmd, "-c", config_filepath, "-l", log_filepath]
traci.start(sumoCmd)


with open(light_data_filepath, mode='w', newline='') as log_file:
    log_writer = csv.writer(log_file)
    log_writer.writerow(["Traffic Light Id", "Controlled Lanes", "Number of Phases"])

    traffic_light_ids = traci.trafficlight.getIDList()

    for tl_id in traffic_light_ids:
        current_state = traci.trafficlight.getRedYellowGreenState(tl_id)
        controlled_lanes = len(traci.trafficlight.getControlledLanes(tl_id))
        num_phases = len(traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0].phases)
        log_writer.writerow([tl_id, controlled_lanes, num_phases])

with open(network_data_filepath, mode='w', newline='') as log_file:
    log_writer = csv.writer(log_file)
    log_writer.writerow([
        "Simulation Time",
        "Total Vehicles",
        "Passenger",
        "Trucks",
        "Buses",
        "Motorcycles",
        "Bicycles",
        "Emergencies",
        "Trailers",
        "Deliveries",
        "Total Fuel Consumption (ml)",
        "Total CO2 Emission (mg)",
        "Total CO Emission (mg)",
        "Total HC Emission (mg)",
        "Total NOx Emission (mg)",
        "Total PMx Emission (mg)",
        "Total Trip Time (s)",
        "Total Delay (s)"
    ])

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        simulation_time = traci.simulation.getTime()

        vehicle_ids = traci.vehicle.getIDList()

        vehicle_counts = {
            "passenger": 0,
            "truck": 0,
            "bus": 0,
            "motorcycle": 0,
            "bicycle": 0,
            "emergency": 0,
            "trailer": 0,
            "delivery": 0
        }

        total_fuel_consumption = 0.0
        total_co2_emission = 0.0
        total_co_emission = 0.0
        total_hc_emission = 0.0
        total_nox_emission = 0.0
        total_pmx_emission = 0.0
        total_trip_time = 0.0
        total_delay = 0.0

        for vid in vehicle_ids:
            vehicle_type = traci.vehicle.getVehicleClass(vid)

            if vehicle_type == "passenger":
                vehicle_counts["passenger"] += 1
            elif vehicle_type == "truck":
                vehicle_counts["truck"] += 1
            elif vehicle_type == "bus":
                vehicle_counts["bus"] += 1
            elif vehicle_type == "motorcycle":
                vehicle_counts["motorcycle"] += 1
            elif vehicle_type == "bicycle":
                vehicle_counts["bicycle"] += 1
            elif vehicle_type == "emergency":
                vehicle_counts["emergency"] += 1
            elif vehicle_type == "trailer":
                vehicle_counts["trailer"] += 1
            elif vehicle_type == "delivery":
                vehicle_counts["delivery"] += 1

            total_fuel_consumption += traci.vehicle.getFuelConsumption(vid)
            total_co2_emission += traci.vehicle.getCO2Emission(vid)
            total_co_emission += traci.vehicle.getCOEmission(vid)
            total_hc_emission += traci.vehicle.getHCEmission(vid)
            total_nox_emission += traci.vehicle.getNOxEmission(vid)
            total_pmx_emission += traci.vehicle.getPMxEmission(vid)
            total_trip_time += traci.vehicle.getAccumulatedWaitingTime(vid)
            total_delay += traci.vehicle.getTimeLoss(vid)

        total_vehicles = sum(vehicle_counts.values())

        log_writer.writerow([
            simulation_time,
            total_vehicles,
            vehicle_counts["passenger"],
            vehicle_counts["truck"],
            vehicle_counts["bus"],
            vehicle_counts["motorcycle"],
            vehicle_counts["bicycle"],
            vehicle_counts["emergency"],
            vehicle_counts["trailer"],
            vehicle_counts["delivery"],
            total_fuel_consumption,
            total_co2_emission,
            total_co_emission,
            total_hc_emission,
            total_nox_emission,
            total_pmx_emission,
            total_trip_time,
            total_delay
        ])

traci.close()

print("Simulation completed and data logged.")