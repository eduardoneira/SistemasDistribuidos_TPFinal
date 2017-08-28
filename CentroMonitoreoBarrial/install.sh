#!/bin/bash

echo "Comienza instalacion de entorno CMB"

cd setup/

./python.sh

./rabbitmq.sh

./python_opencv.sh

cd ..
