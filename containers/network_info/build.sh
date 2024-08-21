DOCKERFILE_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/scripts/network_info/Dockerfile"
IMAGE_NAME="yassinmelsir/simulation-marl-ni:latest"
ROOT_DIR="/Users/yme/York/IRP/sumo_ingolstadt_marl/"

docker build -t $IMAGE_NAME \
  -f $DOCKERFILE_PATH \
  $ROOT_DIR