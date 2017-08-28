#!/bin/bash

echo "Instalando pip"
python3 get-pip.py

echo "Instalando cliente pika"
pip3 install --user pika

echo "Instalando numpy"
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose