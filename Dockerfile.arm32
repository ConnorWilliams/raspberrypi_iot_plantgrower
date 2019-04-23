FROM arm32v7/python:3.7-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV MOSQUITTO_HOST mosquitto
ENV MOSQUITTO_PORT 1883
ENV MOSQUITTO_KEEPALIVE 60
ENV GROW_ID 1
CMD python raspi_consumer.py -h $MOSQUITTO_HOST -p $MOSQUITTO_PORT -k $MOSQUITTO_KEEPALIVE -g $GROW_ID
