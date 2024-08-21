SIF_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/containers/network_info/apptainer/simulation-marl-ni.sif"
SIM_MOUNT_PATH="/users/pdm523/sumo_ingolstadt_marl/simulation:/usr/app/simulation"
DATA_MOUNT_PATH="/users/pdm523/sumo_ingolstadt_marl/data/network_info:/usr/app/data/network_info"

SIM_NAME="2023-06-19"
CONFIG_FILE_PATH="/usr/app/simulation/24h_sim.sumocfg"
DATA_FILE_PATH="/usr/app/data/network_info"


apptainer run \
  --bind $SIM_MOUNT_PATH \
  --bind $DATA_MOUNT_PATH \
  --env SIM_NAME=$SIM_NAME \
  --env CONFIG_FILE_PATH=$CONFIG_FILE_PATH \
  --env DATA_FILE_PATH=$DATA_FILE_PATH \
  $SIF_FILE_PATH