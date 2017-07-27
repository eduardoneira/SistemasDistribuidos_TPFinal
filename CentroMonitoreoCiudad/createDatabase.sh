#!/usr/bin/env bash

sudo -i -u postgres psql -c "CREATE DATABASE cmcdatabase"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cmcdatabase to postgres"
echo "Ingrese el password de postgres y a continuacion ejecute:"
echo "\c cmcdatabase"
echo "Luego ejecute"
echo "postgres# CREATE TABLE Persona(HashPersona char(40) NOT NULL, Estado smallint NOT NULL, CONSTRAINT PK PERSONA PRIMARY_KEY(HashPersona));"
echo "postgres# CREATE TABLE BigPic(HashBigPic char(40) NOT NULL, CONSTRAINT PK_BIGPIC PRIMARY KEY(HashBigPic));"
echo "postgres# CREATE TABLE CropFace(HashCrop char(40) NOT NULL, Lat double precision NOT NULL, Lng double precision NOT NULL, Time timestamp, HashPersona char(40), HashBigPic char(40),CONSTRAINT PK_CROPFACE PRIMARY KEY(HashCrop), CONSTRAINT FK_PERSONA FOREIGN KEY(HashPersona) REFERENCES Persona(HashPersona) on delete cascade on update cascade, CONSTRAINT FK_BIGPIC FOREIGN KEY(HashBigPic) REFERENCES BigPic(HashBigPic) on delete cascade on update cascade);"
echo "Puede ejecutar: \d si desea ver las tablas creadas. PAra salir: \q"
