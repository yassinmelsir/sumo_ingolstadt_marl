import argparse
from collections import defaultdict

from src.procedures.network_info.general import record_light_data, write_light_data, record_step_data, \
    write_vehicle_data
from src.traffic_environment import TrafficEnvironment


def main(sumo_cmd: str, data_file_path: str):
    print(sumo_cmd)
    simulation = TrafficEnvironment(sumo_cmd=sumo_cmd)
    simulation.start_simulation()
    vehicle_data = []
    efficiency_statistics = defaultdict(int)

    # light_data = []
    # record_light_data(light_data=light_data, simulation=simulation)
    # write_light_data(light_data=light_data, data_file_path=data_file_path)

    time_interval = 60
    last_recorded_time = 0

    while simulation.simulation_running:
        simulation.step()
        current_time = simulation.traci.simulation.getTime()

        if current_time - last_recorded_time >= time_interval:
            record_step_data(simulation=simulation, vehicle_data=vehicle_data,
                             efficiency_statistics=efficiency_statistics)
            write_vehicle_data(vehicle_data=vehicle_data, data_file_path=data_file_path)
            last_recorded_time = current_time

    simulation.close_simulation()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Simulation runner")

    argparser.add_argument(
        "--sumo_cmd",
        type=str,
        required=True,
        help="The name of the simulation"
    )
    argparser.add_argument(
        "--data_file_path",
        type=str,
        required=True,
        help="The path to the data store"
    )

    args = argparser.parse_args()

    sumo_cmd = args.sumo_cmd
    data_file_path = args.data_file_path

    main(sumo_cmd=sumo_cmd, data_file_path=data_file_path)
