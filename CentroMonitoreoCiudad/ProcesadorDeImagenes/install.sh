#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "ERROR: Este script se debe correr como root"
    exit
fi

ARGC=$#
if [[ $ARGC == 0 ]]; then
  echo "ERROR: Hay que especificar el sistema operativo en cual instalar. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

if [[ "$1" != "fedora" ]] && [[ "$1" != "arch" ]] && [[ "$1" != "ubuntu" ]] &&   [[ "$1" != "debian" ]]
  then 
  echo "ERROR: Argumento invalido. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

echo "Comienza instalacion de entorno CMC"

mkdir log

cd setup/

./python.sh "$1"

./rabbitmq.sh "$1"

./python_opencv.sh "$1"

cd ..

