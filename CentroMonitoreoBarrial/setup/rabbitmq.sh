#!/bin/bash

echo "Comenzando instalacion rabbitMQ"

sudo rpm rabbitmq-server-3.6.10-1.el7.noarch.rpm

#Para usar mqtt
sudo rabbitmq-plugins enable rabbitmq_mqtt

#Reinicio el servicio
sudo service rabbitmq-server restart
