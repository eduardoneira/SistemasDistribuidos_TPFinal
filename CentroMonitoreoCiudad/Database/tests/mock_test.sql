### Create tables

CREATE TABLE Person(Id int NOT NULL, Filepath char(40) NOT NULL, state char(20) NOT NULL, CONSTRAINT PK_PERSON PRIMARY KEY(Id));
CREATE TABLE BigPic(HashBigPic char(40) NOT NULL, Lat double precision NOT NULL, Lng double precision NOT NULL, Timestmp timestamp, CONSTRAINT PK_BIGPIC PRIMARY KEY(HashBigPic));
CREATE TABLE CropFace(HashCrop char(40) NOT NULL, Id int NOT NULL, HashBigPic char(40),CONSTRAINT PK_CROPFACE PRIMARY KEY(HashCrop), CONSTRAINT FK_PERSON FOREIGN KEY(Id) REFERENCES Person(Id) on delete cascade on update cascade, CONSTRAINT FK_BIGPIC FOREIGN KEY(HashBigPic) REFERENCES BigPic(HashBigPic) on delete cascade on update cascade);


### INSERT

INSERT INTO CropFace VALUES ('hc1',1,'bp1');
INSERT INTO CropFace VALUES ('hc2',1,'bp2');

INSERT INTO BigPic VALUES ('bp1',-34.5884843,-58.3962122,'17-07-2017||01:09:07.434053');
INSERT INTO BigPic VALUES ('bp2',-32.5884843,-56.3962122,'18-07-2017||02:09:07.434053');
