#!/bin/bash

if ! command -v rabbitmq-server > /dev/null 2>&1; then
 
	echo "Instalando dependencias rabbitMQ"

	dnf install erlang
	dnf install logrotate
	dnf install socat

	echo "Comenzando instalacion rabbitMQ"

	rpm -U rabbitmq-server-3.6.10-1.el7.noarch.rpm

  #Para tener un managemente y debug
  rabbitmq-plugins enable rabbitmq_management
	#Para usar mqtt
	rabbitmq-plugins enable rabbitmq_mqtt

fi

#Reinicio el servicio
service rabbitmq-server restart
