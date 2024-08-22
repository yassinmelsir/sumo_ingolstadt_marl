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

COPY ./src /usr/app/src
COPY ./simulation /usr/app/simulation

ENV SUMO_HOME=/usr/share/sumo
ENV PYTHONPATH="${PYTHONPATH}:/usr/app/"
