CONTAINER_NAME="simulation-marl-ni.sif"
DEF_FILE_PATH="/users/pdm523/sumo_ingolstadt_marl/containers/network_info/apptainer/network_info.def"

apptainer --fakeroot build $CONTAINER_NAME $DEF_FILE_PATH