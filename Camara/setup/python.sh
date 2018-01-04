#!/bin/bash

echo "Instalando pip"
sudo python3 get-pip.py

echo "Instalando pygame para control de camara"
pip3 install --user pygame 

echo "Instalando eclipse paho para cliente mqtt"
pip3 install --user paho-mqtt