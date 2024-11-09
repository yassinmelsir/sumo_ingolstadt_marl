from marl.src.environment.traffic_environment import TrafficEnvironment
from marl.src.transformer.classes.train_transformer import TrainTransformer

if __name__ == '__main__':
    gather_data = True
    data_filepath = "/src/transformer/data/transfomer_training_data.npy"
    output_dir = '/Users/yme/Code/York/IRP/sumo_ingolstadt_marl/src/weights/'
    output_filepath = f"{output_dir}transformer_"
    num_heads = 12
    num_layers = 3
    batch_size = 32
    num_epochs = 30
    learning_rate = 0.001
    num_agents = 3
    num_runs = 1
    steps_per_run = 3

    config_file_path = '/Users/yme/Code/York/IRP/sumo_ingolstadt_marl/simulation/24h_sim_10s.sumocfg'
    gui = False
    sumo_cmd = f"sumo -c {config_file_path}"
    ai_control = True

    env = TrafficEnvironment(
        sumo_cmd=sumo_cmd,
        gui=gui,
        ai_control=ai_control
    )

    train = TrainTransformer(
        data_filepath=data_filepath,
        num_heads=num_heads,
        batch_size=batch_size,
        num_layers=num_layers,
        learning_rate=learning_rate,
        output_filepath=output_filepath,
        num_agents=num_agents,
        num_runs=num_runs,
        steps_per_run=steps_per_run,
        env=env,
        gather_data=gather_data
    )

    train.train(num_epochs=num_epochs)
