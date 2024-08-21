docker build -t yassinmelsir/sumo-marl-ni:latest \
  --build-arg SIM_NAME="2023-06-19" \
  --build-arg CONFIG_FILE_PATH="/usr/src/sumo/2023-06-19.sumocfg" \
  --build-arg DATA_FILE_PATH="/usr/src/data" \
  -f /Users/yme/York/IRP/sumo_ingolstadt_marl/scripts/network_info/Dockerfile \
  /Users/yme/York/IRP/sumo_ingolstadt_marl/

docker run yassinmelsir/sumo-marl-ni:latest

#docker push your-dockerhub-username/your-app-name:tag