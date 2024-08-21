DOCKERFILE_PATH="/Users/yme/York/IRP/sumo_ingolstadt_marl/containers/network_info/docker/Dockerfile"
IMAGE_NAME="yassinmelsir/simulation-marl-ni:amd64"
ROOT_DIR="/Users/yme/York/IRP/sumo_ingolstadt_marl/"

docker buildx build -t $IMAGE_NAME \
  -f $DOCKERFILE_PATH \
  --platform linux/amd64 \
  --push \
  $ROOT_DIR