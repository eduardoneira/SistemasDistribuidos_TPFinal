#!/bin/bash

echo "Instalando python 3"
dnf install python3

echo "Instalando pip"
python get-pip.py

echo "Instalando cliente pika"
pip install pika