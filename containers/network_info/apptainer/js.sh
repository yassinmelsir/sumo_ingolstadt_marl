SIM_NAME=${SIM_NAME}
CONTAINER_CONFIG_FILE_PATH=${CONTAINER_CONFIG_FILE_PATH}
CORES=$CORES

LOCAL_DATA_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/data"
LOCAL_SIMULATION_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/simulation"
IMAGE_PATH="/users/pdm523/sumo_ingolstadt_marl/containers/images/simulation-marl-ni.sif"

CONTAINER_DATA_FILE_PATH="/usr/app/data"
CONTAINER_SIMULATION_FILE_PATH="/usr/app/simulation"

SUMO_CMD="/usr/bin/sumo -c $CONTAINER_CONFIG_FILE_PATH --threads $CORES --device.rerouting.threads $CORES --verbose true"

RUN_SCRIPT="python3 /usr/app/src/procedures/network_info/main.py \
                      --sumo_cmd \"${SUMO_CMD}\" \
                      --data_file_path ${CONTAINER_DATA_FILE_PATH}"

LOCAL_DATA_FILE_PATH="$LOCAL_DATA_FILE_PATH/$SIM_NAME"

SIMULATION_MOUNT_PATH="$LOCAL_SIMULATION_FILE_PATH:$CONTAINER_SIMULATION_FILE_PATH"
DATA_MOUNT_PATH="$LOCAL_DATA_FILE_PATH:$CONTAINER_DATA_FILE_PATH"

module load Apptainer/latest

mkdir $LOCAL_DATA_FILE_PATH

apptainer -d exec --bind "$SIMULATION_MOUNT_PATH" \
                  --bind "$DATA_MOUNT_PATH" \
                  $IMAGE_PATH sh -c "$RUN_SCRIPT"