IMAGE_NAME="yassinmelsir/simulation-marl-ni:amd64"
IMAGE_PATH="/users/pdm523/sumo_ingolstadt_marl/containers/images/simulation-marl-ni.sif"

module load Apptainer/latest

apptainer build $IMAGE_PATH "docker://$IMAGE_NAME"
