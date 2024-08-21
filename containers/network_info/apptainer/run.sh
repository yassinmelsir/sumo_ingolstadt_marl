SIM_NAME="2023-06-19"
CONFIG_FILE_PATH="/usr/app/simulation/24h_sim.sumocfg"
DATA_FILE_PATH="/usr/app/data/network_info"
SIMULATION_MOUNT_PATH="/users/pdm523/sumo_ingolstadt_marl/simulation:/usr/app/simulation"
DATA_MOUNT_PATH="/users/pdm523/sumo_ingolstadt_marl/data/network_info:/usr/app/data/network_info"
IMAGE_PATH="/users/pdm523/sumo_ingolstadt_marl/containers/images/simulation-marl-ni.sif"

apptainer exec --bind $SIMULATION_MOUNT_PATH \
               --bind $DATA_MOUNT_PATH \
               $IMAGE_PATH \
               sh -c "cd /usr/app/ && \
                      python3 src/procedures/network_info/network_info.py \
                      --sim_name $SIM_NAME \
                      --config_file_path $CONFIG_FILE_PATH \
                      --data_file_path $DATA_FILE_PATH"