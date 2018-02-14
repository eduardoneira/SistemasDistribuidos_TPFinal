#!/bin/bash

if ! command -v rabbitmq-server > /dev/null 2>&1; then
 
	echo "Instalando dependencias rabbitMQ"

	sudo apt-get install erlang
	sudo apt-get install logrotate
	sudo apt-get install socat

	echo "Comenzando instalacion rabbitMQ"

	rpm -U rabbitmq-server-3.6.10-1.el7.noarch.rpm

  #Para tener un managemente y debug
  sudo rabbitmq-plugins enable rabbitmq_management
	#Para usar mqtt
	sudo rabbitmq-plugins enable rabbitmq_mqtt

	#copy configuration to path
	sudo cp ../../Utils/rabbitmq.config /etc/rabbitmq/

fi

#Reinicio el servicio
sudo service rabbitmq-server restart
