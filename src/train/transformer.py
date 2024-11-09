import numpy as np

from marl.src.environment.traffic_environment import TrafficEnvironment
from marl.src.transformer.classes.env_data import EnvData
from marl.src.transformer.classes.train_transformer import TrainTransformer

if __name__ == '__main__':
    gather_data = True
    data_output_filepath = "/src/transformer/data/transfomer_training_data.npy"
    output_dir = '/Users/yme/Code/York/IRP/sumo_ingolstadt_marl/src/weights/'
    output_filepath = f"{output_dir}transformer_"
    num_heads = 12
    num_layers = 3
    batch_size = 32
    num_epochs = 30
    learning_rate = 0.001
    num_agents = 3
    num_runs = 1
    steps_per_run = 1

    config_file_paths = [
        '/Users/yme/Code/York/IRP/sumo_ingolstadt_marl/simulation/24h_sim.sumocfg',
        '/Users/yme/Code/York/IRP/sumo_ingolstadt_marl/simulation/Ingolstadt_SUMO_365/2023-06-19.sumocfg'
    ]

    gui = False
    begin = 21600
    ai_control = True

    sumo_runs = []
    for config_file_path in config_file_paths:
        sumo_cmd = f"sumo -c {config_file_path} --begin {begin}"
        env = TrafficEnvironment(
            sumo_cmd=sumo_cmd,
            gui=gui,
            ai_control=ai_control
        )

        env_data = EnvData(
            num_agents=num_agents,
            num_runs=num_runs,
            steps_per_run=steps_per_run,
            env=env,
            data_filepath=data_output_filepath,
            num_heads=num_heads
        )
        env_data.gather_data()
        new_data = env_data.shape_data()
        sumo_runs.append(new_data[0])

        env.close_simulation()

    max_obs_len = max([step.shape[0] for run in sumo_runs for step in run])
    for index, run in enumerate(sumo_runs):
        padding = np.zeros(shape=(1, num_heads - (run.shape[0]) % num_heads))
        sumo_runs[index] = np.concatenate((run, padding))

    breakpoint()

    train = TrainTransformer(
        num_heads=num_heads,
        batch_size=batch_size,
        num_layers=num_layers,
        learning_rate=learning_rate,
        output_filepath=output_filepath,
        data=sumo_runs
    )

    train.train(num_epochs=num_epochs)
