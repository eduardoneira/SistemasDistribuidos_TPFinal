#!/bin/bash

echo "Instalando python 3"
dnf install python3

echo "Instalando pip"
python3 get-pip.py

echo "Instalando pygame para control de camara"
pip3 install pygame --user

echo "Instalando eclipse paho para cliente mqtt"
pip install paho-mqtt
cp -R /lib/python2.7/site-packages/paho /lib/python3.6/site-packages/