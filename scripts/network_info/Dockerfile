FROM python:3.9-slim

WORKDIR /usr/src

COPY ./src ./

RUN apt-get update && apt-get install -y sumo

RUN pip install --no-cache-dir traci numpy

ENV PYTHONPATH="${PYTHONPATH}:/usr/"

# Accept build arguments
ARG SIM_NAME
ARG CONFIG_FILE_PATH
ARG DATA_FILE_PATH

# Set environment variables for runtime
ENV SIM_NAME=${SIM_NAME}
ENV CONFIG_FILE_PATH=${CONFIG_FILE_PATH}
ENV DATA_FILE_PATH=${DATA_FILE_PATH}

CMD ["sh", "-c", \
    "echo SIM_NAME=$SIM_NAME CONFIG_FILE_PATH=$CONFIG_FILE_PATH DATA_FILE_PATH=$DATA_FILE_PATH && \
    python procedures/network_info/network_info.py  \
    --sim_name $SIM_NAME --config_file_path $CONFIG_FILE_PATH --data_file_path $DATA_FILE_PATH"]