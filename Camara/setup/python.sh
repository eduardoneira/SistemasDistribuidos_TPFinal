#!/bin/bash

echo "Instalando python 3"
dnf install python3

echo "Instalando pip"
python3 get-pip.py

echo "Instalando cliente pika"
pip3 install pika --user

echo "Instalando pygame para control de camara"
pip3 install pygame --user