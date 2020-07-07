#!/bin/bash
app="docker.sdg.api"
docker build -t ${app} .
#sudo docker run -it -p 5000:5000 --rm --name=docker.sdg.api docker.sdg.api
