#!/bin/python3

import unittest
import sys
import psycopg2
import json
from datetime import datetime
sys.path.insert(0, '../../../')
from Utils.Hash import compute_sha1_from_file
LEGALPROBLEMS= 0
class TestDatabase(unittest.TestCase):

    def setUp(self):
        with open('../config.json') as f:
            conf = json.load(f)
            connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
            self.connection = psycopg2.connect(connection_str)
        self.cursor = self.connection.cursor()
        self.hash_big_pic = compute_sha1_from_file('got.jpg');
        self.hash_person = compute_sha1_from_file('jon_snow3.jpg')
        self.Id = 0
        self.hash_crop = compute_sha1_from_file('jon_snow2.jpg')
        self.lat = -34.5884843
        self.lng = -58.3962122
        self.timestamp= datetime.now()
        self.state = LEGALPROBLEMS
        self.cursor.execute("""INSERT INTO Person (Id, Filepath, state) VALUES (%s, %s, %s)""",(self.Id, self.hash_person, self.state))
        self.cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(self.hash_big_pic, self.lat, self.lng, self.timestamp))
        self.cursor.execute("""INSERT INTO CropFace (HashCrop, Id, HashBigPic) VALUES (%s, %s, %s)""",(self.hash_crop,self.Id, self.hash_big_pic))
    def tearDown(self):
        self.cursor.close()
        self.connection.close()

    def test_find_one_tuple_from_cropface_table(self):
        self.cursor.execute("SELECT CropFace.HashCrop FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertTrue(len(rows) == 1)
    def test_find_hash_crop_from_cropface_table(self):
        self.cursor.execute("SELECT CropFace.HashCrop FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.hash_crop)
    def test_find_hash_person_from_cropface_table(self):
        self.cursor.execute("SELECT CropFace.Id FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.Id)
    def test_find_hash_big_pic_from_cropface_table(self):
        self.cursor.execute("SELECT CropFace.HashBigPic FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.hash_big_pic)
    def test_find_all_fields_from_person_table(self):
        self.cursor.execute("SELECT * FROM Person WHERE  Person.Id = %s", (self.Id,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.Id)
        self.assertEqual(rows[0][1], self.hash_person)
        self.assertEqual(rows[0][2], self.state)
    def test_find_all_fields_from_cropface_table(self):
        self.cursor.execute("SELECT * FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.hash_crop)
        self.assertEqual(rows[0][1], self.Id)
        self.assertEqual(rows[0][2], self.hash_big_pic)
    def test_find_all_fields_from_bigpic_table(self):
        self.cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic = %s", (self.hash_big_pic,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.hash_big_pic)
        self.assertEqual(rows[0][1], self.lat)
        self.assertEqual(rows[0][2], self.lng)
        self.assertEqual(rows[0][3], self.timestamp)
    def test_person_in_new_bigpic(self):
        self.hash_big_pic_new = compute_sha1_from_file('got2.jpg');
        self.hash_crop_new = compute_sha1_from_file('jon_snow1.jpg')
        self.lat_new = -34.5895876
        self.lng_new = -58.3562457
        self.timestamp_new= datetime.now()
        self.cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(self.hash_big_pic_new, self.lat_new, self.lng_new, self.timestamp_new))
        self.cursor.execute("""INSERT INTO CropFace (HashCrop, Id, HashBigPic) VALUES (%s, %s, %s)""",(self.hash_crop_new,self.Id, self.hash_big_pic_new))
        self.cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic IN (SELECT CropFace.HashBigPic FROM CropFace WHERE CropFace.Id = %s)", (self.Id,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[1][0], self.hash_big_pic)
        self.assertEqual(rows[1][1], self.lat)
        self.assertEqual(rows[1][2], self.lng)
        self.assertEqual(rows[1][3], self.timestamp)
        self.assertEqual(rows[0][0], self.hash_big_pic_new)
        self.assertEqual(rows[0][1], self.lat_new)
        self.assertEqual(rows[0][2], self.lng_new)
        self.assertEqual(rows[0][3], self.timestamp_new)
    def test_delete_Person(self):
        self.cursor.execute("DELETE FROM Person WHERE Person.Id= %s",(self.Id,))
        self.cursor.execute("SELECT Person.Id FROM Person WHERE  Person.Id = %s", (self.Id,))
        rows = self.cursor.fetchall()
        self.assertTrue(len(rows) == 0)
        self.cursor.execute("SELECT CropFace.HashCrop FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
        rows = self.cursor.fetchall()
        self.assertTrue(len(rows) == 0)
        self.cursor.execute("SELECT BigPic.HashBigPic FROM BigPic WHERE  BigPic.HashBigPic = %s", (self.hash_big_pic,))
        rows = self.cursor.fetchall()
        self.assertTrue(len(rows) == 1)
    def test_location_cropface_and_bigpic_from_a_person(self):
        self.cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic = (SELECT CropFace.HashBigPic FROM CropFace WHERE CropFace.Id = %s)", (self.Id,))
        rows = self.cursor.fetchall()
        self.assertEqual(rows[0][0], self.hash_big_pic)
        self.assertEqual(rows[0][1], self.lat)
        self.assertEqual(rows[0][2], self.lng)
        self.assertEqual(rows[0][3], self.timestamp)
    def test_delete_big_pic(self):
        self.cursor.execute("DELETE FROM BigPic WHERE BigPic.HashBigPic= %s",(self.hash_big_pic,))
        self.cursor.execute("SELECT BigPic.HashBigPic FROM BigPic WHERE  BigPic.HashBigPic = %s", (self.hash_big_pic,))
        rows = self.cursor.fetchall()
        self.assertTrue(len(rows) == 0)
if __name__ == '__main__':
  unittest.main()
