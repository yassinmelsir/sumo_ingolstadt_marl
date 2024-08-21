FROM python:3.9-slim

WORKDIR /usr/src

COPY ../../src ./src

RUN apt-get update && apt-get install -y sumo

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/procedures/network_info/network_info.py"]