#!/bin/bash

echo "Instalando dependencias rabbitMQ"

dnf install erlang
dnf install logrotate
dnf install socat

echo "Comenzando instalacion rabbitMQ"

rpm -U rabbitmq-server-3.6.10-1.el7.noarch.rpm

#Para usar mqtt
rabbitmq-plugins enable rabbitmq_mqtt

#Reinicio el servicio
service rabbitmq-server restart
