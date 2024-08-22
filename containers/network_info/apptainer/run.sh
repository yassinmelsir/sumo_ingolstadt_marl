SIM_NAME="network_info/2023-06-19"
LOCAL_DATA_FILE_PATH="/user/pdm523/sumo_ingolstadt_marl/data"
LOCAL_SIMULATION_FILE_PATH="/user/pdm523/sumo_ingolstadt_marl/simulation"
IMAGE_NAME="yassinmelsir/simulation-marl-ni:amd64"

SUMO_CMD="/usr/bin/sumo -c $CONTAINER_CONFIG_FILE_PATH --threads 2 --device.rerouting.threads 1 --verbose true --end 1000"

RUN_SCRIPT="python3 /usr/app/src/procedures/network_info/main.py \
                      --sumo_cmd \"${SUMO_CMD}\" \
                      --data_file_path ${CONTAINER_DATA_FILE_PATH}"

CONTAINER_CONFIG_FILE_PATH="/usr/app/simulation/Ingolstadt SUMO 365/2023-06-19.sumocfg"
CONTAINER_DATA_FILE_PATH="/usr/app/data/"
CONTAINER_SIMULATION_FILE_PATH="/usr/app/simulation/"

SIMULATION_MOUNT_PATH="$LOCAL_SIMULATION_FILE_PATH:$CONTAINER_SIMULATION_FILE_PATH"
DATA_MOUNT_PATH="$LOCAL_DATA_FILE_PATH/$SIM_NAME:$CONTAINER_DATA_FILE_PATH"

apptainer exec --bind $SIMULATION_MOUNT_PATH \
               --bind $DATA_MOUNT_PATH \
               $IMAGE_NAME sh -c "$RUN_SCRIPT"