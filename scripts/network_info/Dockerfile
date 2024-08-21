FROM ubuntu:latest

WORKDIR /usr/app

RUN apt-get update && apt-get install -y \
    sumo \
    sumo-tools \
    sumo-doc \
    python3-pip \
    build-essential \
    python3-dev \
    python3-numpy

ENV SUMO_HOME=/usr/share/sumo
ENV PYTHONPATH="${PYTHONPATH}:/usr/app/"


COPY ./src /usr/app/src
COPY ./simulation /usr/app/simulation

ARG SIM_NAME
ARG CONFIG_FILE_PATH
ARG DATA_FILE_PATH

ENV SIM_NAME=${SIM_NAME}
ENV CONFIG_FILE_PATH=${CONFIG_FILE_PATH}
ENV DATA_FILE_PATH=${DATA_FILE_PATH}


CMD ["sh", "-c", \
    "python3 src/procedures/network_info/network_info.py  \
    --sim_name $SIM_NAME --config_file_path $CONFIG_FILE_PATH --data_file_path $DATA_FILE_PATH"]