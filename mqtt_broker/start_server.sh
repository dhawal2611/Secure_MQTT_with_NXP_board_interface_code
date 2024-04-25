#!/bin/bash

# Get the actual workspace folder path
WORKSPACE_FOLDER=$(pwd)

# Replace the placeholder in mosquitto.conf template with the actual path
sed "s|%WORKSPACE_FOLDER%|${WORKSPACE_FOLDER}|g" conf/template.conf.template > conf/mosquitto_c.conf

mosquitto -c ${WORKSPACE_FOLDER}/conf/mosquitto_c.conf  -v