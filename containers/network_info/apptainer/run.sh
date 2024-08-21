SIM_NAME="2023-06-19"
CONFIG_FILE_PATH="/usr/app/simulation/24h_sim.sumocfg"
DATA_FILE_PATH="/usr/app/data/network_info"
SIMULATION_MOUNT_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/simulation:/usr/app/simulation"
DATA_MOUNT_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/data/network_info:/usr/app/data/network_info"
IMAGE_NAME="yassinmelsir/simulation-marl-ni:latest"

apptainer run -e SIM_NAME=$SIM_NAME \
           -e CONFIG_FILE_PATH=$CONFIG_FILE_PATH \
           -e DATA_FILE_PATH=$DATA_FILE_PATH  \
           -v $SIMULATION_MOUNT_PATH \
           -v $DATA_MOUNT_PATH \
           $IMAGE_NAME
