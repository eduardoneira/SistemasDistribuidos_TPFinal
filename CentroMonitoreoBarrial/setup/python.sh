#!/bin/bash

echo "Instalando pip"
python3 get-pip.py

echo "Instalando cliente pika"
pip3 install --user pika

sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev

echo "Instalando numpy"
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose scikit-image dlib
