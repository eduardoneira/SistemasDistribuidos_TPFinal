#!/bin/python3

import sys
import psycopg2
import json
from datetime import datetime
sys.path.insert(0, '../')
from Utils.Hash import compute_sha1_from_file

def loadBigPicAndCrop(filename, cropFile, lat, lng):
    hash_big_pic = compute_sha1_from_file(filename);
    hash_crop = compute_sha1_from_file(cropFile)
    timestamp= datetime.now()
    cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(hash_big_pic, lat, lng, timestamp))
    cursor.execute("""INSERT INTO CropFace (HashCrop, Id, HashBigPic) VALUES (%s, %s, %s)""",(hash_crop, 1, hash_big_pic))

def loadCrop():
    cursor.execute("""INSERT INTO CropFace (HashCrop, Id, HashBigPic) VALUES (%s, %s, %s)""",(hash_crop, 1, hash_big_pic))
if __name__ == '__main__':
  with open('./config.json') as f:
      conf = json.load(f)
      connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
      connection = psycopg2.connect(connection_str)
      connection.autocommit = True
      cursor = connection.cursor()
      loadBigPicAndCrop('./BigPic/1.jpg', './CropFace/crop1.jpg',-34.593390,-58.390049);
      loadBigPicAndCrop('./BigPic/3.jpg','./CropFace/crop2.jpg',-34.597311,-58.371917);
      loadBigPicAndCrop('./BigPic/4.jpg','./CropFace/crop3.jpg',-34.617528,-58.368323);
      loadBigPicAndCrop('./BigPic/5.jpg','./CropFace/crop4.jpg',-34.590844, -58.378730);
      loadBigPicAndCrop('./BigPic/6.jpg','./CropFace/crop5.jpg',-34.585120, -58.391604);
      loadBigPicAndCrop('./BigPic/8.jpg','./CropFace/crop6.jpg',-34.599605, -58.450313);
      cursor.close()
      connection.close()
