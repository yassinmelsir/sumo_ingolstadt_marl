import csv
import os
from collections import defaultdict
from typing import List


def write_light_data(light_data: List, data_file_path: str):
    light_data_filepath = os.path.join(data_file_path, "light_info.csv")
    os.makedirs(os.path.dirname(light_data_filepath), exist_ok=True)

    with open(light_data_filepath, mode='w', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(["Traffic Light Id", "Controlled Lanes", "Number of Phases"])
        log_writer.writerows(light_data)

def write_vehicle_data(vehicle_data: List, data_file_path: str):
    network_data_filepath = os.path.join(data_file_path, "vehicle_data.csv")
    os.makedirs(os.path.dirname(network_data_filepath), exist_ok=True)

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
        log_writer.writerows(vehicle_data)

def record_light_data(light_data, simulation):
    traffic_light_ids = simulation.traci.trafficlight.getIDList()

    for tl_id in traffic_light_ids:
        controlled_lanes = len(simulation.traci.trafficlight.getControlledLanes(tl_id))
        num_phases = len(simulation.traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0].phases)
        light_data.append([tl_id, controlled_lanes, num_phases])

def record_step_data(simulation, vehicle_data):
    simulation_time = simulation.traci.simulation.getTime()
    vehicle_ids = simulation.traci.vehicle.getIDList()

    vehicle_counts = defaultdict(int)
    total_fuel_consumption = total_co2_emission = total_co_emission = 0.0
    total_hc_emission = total_nox_emission = total_pmx_emission = 0.0
    total_trip_time = total_delay = 0.0

    for vid in vehicle_ids:
        vehicle_type = simulation.traci.vehicle.getVehicleClass(vid)
        vehicle_counts[vehicle_type] += 1

        total_fuel_consumption += simulation.traci.vehicle.getFuelConsumption(vid)
        total_co2_emission += simulation.traci.vehicle.getCO2Emission(vid)
        total_co_emission += simulation.traci.vehicle.getCOEmission(vid)
        total_hc_emission += simulation.traci.vehicle.getHCEmission(vid)
        total_nox_emission += simulation.traci.vehicle.getNOxEmission(vid)
        total_pmx_emission += simulation.traci.vehicle.getPMxEmission(vid)
        total_trip_time += simulation.traci.vehicle.getAccumulatedWaitingTime(vid)
        total_delay += simulation.traci.vehicle.getTimeLoss(vid)

    total_vehicles = sum(vehicle_counts.values())

    vehicle_data.append([
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