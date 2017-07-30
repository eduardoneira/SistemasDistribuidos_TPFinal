#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "ERROR: Este script se debe correr como root"
    exit
fi

echo "Comienza instalacion de entorno CMB"

mkdir log

cd setup/

./python.sh

./rabbitmq.sh

./python_opencv.sh

cd ..
