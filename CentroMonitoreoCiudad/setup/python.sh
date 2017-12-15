#!/bin/bash

echo "Instalando python 3"
if [[ "$1" == "fedora" ]]; then
  sudo dnf install python3
  sudo dnf install python3-tkinter
elif [[ "$1" == "arch" ]]; then
  sudo pacman -S python3
elif [[ "$1" == "debian" ]] || [[ "$1" == "ubuntu" ]]; then
  sudo apt-get install python3
fi

echo "Instalando pip"
sudo python3 get-pip.py

echo "Instalando cliente pika"
pip3 install --user pika

echo "Instalando numpy & more"
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose   cachetools