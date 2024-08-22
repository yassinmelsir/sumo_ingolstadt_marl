SIM_NAME="network_info/2023-06-19"
CONFIG_FILE_PATH="/usr/app/simulation/24h_sim.sumocfg"
CONTAINER_DATA_FILE_PATH="/usr/app/data/"
CONTAINER_SIMULATION_FILE_PATH="/usr/app/simulation"
LOCAL_DATA_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/data/$SIM_NAME"
LOCAL_SIMULATION_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/simulation"

SIMULATION_MOUNT_PATH="$LOCAL_SIMULATION_FILE_PATH:$CONTAINER_SIMULATION_FILE_PATH"
DATA_MOUNT_PATH="$LOCAL_DATA_FILE_PATH:$CONTAINER_DATA_FILE_PATH"

SUMO_CMD="sumo -c $CONFIG_FILE_PATH --threads=4 --threads.rerouting=2 --verbose=true --end=2000"

RUN_SCRIPT="python3 /usr/app/src/procedures/network_info/main.py \
                      --sumo_cmd $SUMO_CMD \
                      --config_file_path $CONFIG_FILE_PATH \
                      --data_file_path $CONTAINER_DATA_FILE_PATH"

apptainer exec --bind $SIMULATION_MOUNT_PATH \
               --bind $DATA_MOUNT_PATH \
               $IMAGE_PATH \
               sh -c $RUN_SCRIPT