#!/usr/bin/env bash

sudo -i -u postgres psql -c "CREATE DATABASE cmcdatabase"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cmcdatabase to postgres"
echo "Ingrese el password de postgres y a continuacion ejecute:"
echo "\c cmcdatabase"
echo "Luego ejecute"
echo "postgres# CREATE TABLE Person(HashPerson char(40) NOT NULL, state smallint NOT NULL, CONSTRAINT PK_PERSON PRIMARY KEY(HashPerson));"
echo "postgres# CREATE TABLE BigPic(HashBigPic char(40) NOT NULL, Lat double precision NOT NULL, Lng double precision NOT NULL, Timestmp timestamp, CONSTRAINT PK_BIGPIC PRIMARY KEY(HashBigPic));"
echo "postgres# CREATE TABLE CropFace(HashCrop char(40) NOT NULL, HashPerson char(40), HashBigPic char(40),CONSTRAINT PK_CROPFACE PRIMARY KEY(HashCrop), CONSTRAINT FK_PERSON FOREIGN KEY(HashPerson) REFERENCES Person(HashPerson) on delete cascade on update cascade, CONSTRAINT FK_BIGPIC FOREIGN KEY(HashBigPic) REFERENCES BigPic(HashBigPic) on delete cascade on update cascade);"
echo "Puede ejecutar: \d si desea ver las tablas creadas. Para salir: \q"
