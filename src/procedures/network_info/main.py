import argparse
from src.procedures.network_info.general import record_light_data, write_light_data, record_step_data, \
    write_vehicle_data
from src.traffic_environment import TrafficEnvironment


def main(sumo_cmd: str, data_file_path: str):
    print(sumo_cmd)
    simulation = TrafficEnvironment(sumo_cmd=sumo_cmd)
    simulation.start_simulation()
    light_data = []
    vehicle_data = []

    record_light_data(light_data=light_data, simulation=simulation)
    write_light_data(light_data=light_data, data_file_path=data_file_path)

    while simulation.simulation_running:
        simulation.step()
        record_step_data(simulation=simulation, vehicle_data=vehicle_data)

    simulation.close_simulation()

    write_vehicle_data(vehicle_data=vehicle_data, data_file_path=data_file_path)

    print("Simulation completed and data written!")


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
