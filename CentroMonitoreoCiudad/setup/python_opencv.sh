#!/bin/bash

if [[ "$#" == 0 ]]; then
  echo "ERROR: Hay que especificar el sistema operativo en cual instalar. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

echo "Instalando openCV"

if [[ "$1" == "fedora" ]]; then
  ./install_opencv_fedora.sh
elif [[ "$1" == "arch" ]]; then
  pacman -S opencv*
elif [[ "$1" == "debian" ]] || [[ "$1" == "ubuntu" ]]; then
  ./install_opencv_ubuntu.sh
fi