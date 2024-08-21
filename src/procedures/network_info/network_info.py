import csv
import os
import argparse

from src.traffic_environment import TrafficEnvironment

def main(sim_name: str, config_file_path: str, data_file_path: str):
    simulation = TrafficEnvironment(sim_name=sim_name, config_file_path=config_file_path, data_file_path=data_file_path)
    network_data_filepath = os.path.join(simulation.data_file_path, "vehicle_data.csv")
    light_data_filepath = os.path.join(simulation.data_file_path, "light_info.csv")
    os.makedirs(os.path.dirname(light_data_filepath), exist_ok=True)
    os.makedirs(os.path.dirname(network_data_filepath), exist_ok=True)

    simulation.start_simulation()

    with open(light_data_filepath, mode='w', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(["Traffic Light Id", "Controlled Lanes", "Number of Phases"])

        traffic_light_ids = simulation.traci.trafficlight.getIDList()

        for tl_id in traffic_light_ids:
            current_state = simulation.traci.trafficlight.getRedYellowGreenState(tl_id)
            controlled_lanes = len(simulation.traci.trafficlight.getControlledLanes(tl_id))
            num_phases = len(simulation.traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0].phases)
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

        while simulation.simulation_running:
            simulation.step()

            simulation_time = simulation.traci.simulation.getTime()
            vehicle_ids = simulation.traci.vehicle.getIDList()

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
                vehicle_type = simulation.traci.vehicle.getVehicleClass(vid)

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

                total_fuel_consumption += simulation.traci.vehicle.getFuelConsumption(vid)
                total_co2_emission += simulation.traci.vehicle.getCO2Emission(vid)
                total_co_emission += simulation.traci.vehicle.getCOEmission(vid)
                total_hc_emission += simulation.traci.vehicle.getHCEmission(vid)
                total_nox_emission += simulation.traci.vehicle.getNOxEmission(vid)
                total_pmx_emission += simulation.traci.vehicle.getPMxEmission(vid)
                total_trip_time += simulation.traci.vehicle.getAccumulatedWaitingTime(vid)
                total_delay += simulation.traci.vehicle.getTimeLoss(vid)

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

    simulation.close_simulation()

    print("Simulation completed and data logged.")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Simulation runner")

    argparser.add_argument(
        "--sim_name",
        type=str,
        required=True,
        help="The name of the simulation"
    )
    argparser.add_argument(
        "--config_file_path",
        type=str,
        required=True,
        help="The path to the configuration file"
    )

    argparser.add_argument(
        "--data_file_path",
        type=str,
        required=True,
        help="The path to the configuration file"
    )

    args = argparser.parse_args()

    sim_name = args.sim_name
    config_file_path = args.config_file_path
    data_file_path = args.data_file_path

    print(f"Simulation Name: {sim_name}")
    print(f"Configuration File Path: {config_file_path}")
    print(f"Data File Path: {data_file_path}")


    main(sim_name=sim_name, config_file_path=config_file_path, data_file_path=data_file_path)