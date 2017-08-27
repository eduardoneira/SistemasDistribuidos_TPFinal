#!/usr/bin/env bash

sudo -i -u postgres psql -c "CREATE DATABASE cmcdatabase"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cmcdatabase to postgres"
echo "Ingrese el password de postgres y a continuacion ejecute:"
echo "postgres# \c cmcdatabase"
echo "Luego ejecute"
echo "cmcdatabase# CREATE TABLE Person(Id int NOT NULL, dni int NOT NULL, state char(20) NOT NULL, name char(20) NOT NULL, surname char(20) NOT NULL, CONSTRAINT PK_PERSON PRIMARY KEY(Id));"
echo "cmcdatabase# CREATE TABLE BigPic(HashBigPic char(40) NOT NULL, Lat double precision NOT NULL, Lng double precision NOT NULL, Timestmp timestamp, CONSTRAINT PK_BIGPIC PRIMARY KEY(HashBigPic));"
echo "cmcdatabase# CREATE TABLE CropFace(HashCrop char(40) NOT NULL, Id int NOT NULL, HashBigPic char(40),CONSTRAINT PK_CROPFACE PRIMARY KEY(HashCrop), CONSTRAINT FK_PERSON FOREIGN KEY(Id) REFERENCES Person(Id) on delete cascade on update cascade, CONSTRAINT FK_BIGPIC FOREIGN KEY(HashBigPic) REFERENCES BigPic(HashBigPic) on delete cascade on update cascade);"
echo "Puede ejecutar: \d si desea ver las tablas creadas. Para salir: \q"
