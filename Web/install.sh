#!/usr/bin/env bash

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

echo "Comienza instalacion de entorno WEB"

cd setup/

./python.sh "$1"

cd ..