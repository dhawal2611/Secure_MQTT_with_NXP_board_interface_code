# Use a base image
FROM ubuntu:latest

# Install required dependencies
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y git \ 
    build-essential \
    xsltproc \
    cmake libssl-dev \
    libwebsockets-dev \
    docbook-xsl \
    vim \
    mosquitto \
    mosquitto-clients \
    openssl \
    libmosquitto-dev

EXPOSE 1883

EXPOSE 8883

