#!/bin/bash

if [[ "$#" == 0 ]]; then
  echo "ERROR: Hay que especificar el sistema operativo en cual instalar. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

echo "Instalando python 3"
if [[ "$1" == "fedora" ]]; then
  dnf install python3
  dnf install python3-tkinter
elif [[ "$1" == "arch" ]]; then
  pacman -S python3
elif [[ "$1" == "debian" ]] || [[ "$1" == "ubuntu" ]]; then
  apt-get install python3
fi

echo "Instalando pip"
python3 get-pip.py

echo "Instalando cliente pika"
pip3 install pika

echo "Instalando numpy"
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose