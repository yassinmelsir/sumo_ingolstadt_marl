SIM_NAME="network_info/2023-06-19"
CONFIG_FILE_PATH="/usr/app/simulation/24h_sim.sumocfg"
CONTAINER_DATA_FILE_PATH="/usr/app/data/"
CONTAINER_SIMULATION_FILE_PATH="/usr/app/simulation/"

LOCAL_DATA_FILE_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/data"
LOCAL_SIMULATION_FILE_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/simulation"

IMAGE_NAME="yassinmelsir/simulation-marl-ni:latest"

SUMO_CMD="/usr/bin/sumo -c $CONFIG_FILE_PATH --threads 2 --device.rerouting.threads 1 --verbose true --end 2000"

RUN_SCRIPT="python3 /usr/app/src/procedures/network_info/main.py \
                      --sumo_cmd \"${SUMO_CMD}\" \
                      --data_file_path ${CONTAINER_DATA_FILE_PATH}"

SIMULATION_MOUNT_PATH="$LOCAL_SIMULATION_FILE_PATH:$CONTAINER_SIMULATION_FILE_PATH"
DATA_MOUNT_PATH="$LOCAL_DATA_FILE_PATH/$SIM_NAME:$CONTAINER_DATA_FILE_PATH"

docker run -v "$SIMULATION_MOUNT_PATH" \
           -v "$DATA_MOUNT_PATH" \
           $IMAGE_NAME bash -c "$RUN_SCRIPT"