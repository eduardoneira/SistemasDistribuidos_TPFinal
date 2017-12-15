#!/bin/bash

if [[ "$#" == 0 ]]; then
  echo "ERROR: Hay que especificar el sistema operativo en cual instalar. Puede ser: fedora, arch, ubuntu o debian"
  exit
fi

if ! command -v rabbitmq-server > /dev/null 2>&1; then
 
	echo "Instalando dependencias rabbitMQ"

	if [[ "$1" == "fedora" ]]; then
  	dnf install erlang
		dnf install logrotate
		dnf install socat
	elif [[ "$1" == "arch" ]]; then
	  pacman -S erlang
	  pacman -S logrotate
	  pacman -S socat
	elif [[ "$1" == "debian" ]] || [[ "$1" == "ubuntu" ]]; then
	  apt-get install erlang
		apt-get install logrotate
		apt-get install socat
	fi

	echo "Comenzando instalacion rabbitMQ"

	rpm -U rabbitmq-server-3.6.10-1.el7.noarch.rpm

  #Para tener un managemente y debug
  rabbitmq-plugins enable rabbitmq_management
	#Para usar mqtt
	rabbitmq-plugins enable rabbitmq_mqtt

  cp ../../Utils/rabbitmq.config /etc/rabbitmq/
fi

#Reinicio el servicio
service rabbitmq-server restart
