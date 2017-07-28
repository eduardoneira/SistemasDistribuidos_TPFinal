from flask import (
    jsonify,
    render_template
)

import os
import sys
sys.path.insert(0, '../../')
import Utils.const
from Utils.Hash import Sha1
import json
from werkzeug import secure_filename
from flask_googlemaps import Map, icons

class Manager(object):
    def __init__(self, file, basedir):
        with open('../config.json') as f:
            conf = json.load(f)
            connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
            self.connection = psycopg2.connect(connection_str)
        self.cursor = self.connection.cursor()
        self.sha1 = Sha1()
        self.file=file
        self.filename = secure_filename(file.filename)
        self.updir = os.path.join(basedir, 'upload/')
        self.filePath= os.path.join(self.updir, self.filename)
        self.fileExists = (self.feature_matcher.compare_to_all_faces(self.filePath) == ONEMATCH) #os.path.isfile(self.filePath)
    def responseAlreadyExists(self):
        img_path = self.feature_matcher.getMatch() #Deberia devolver el path de la foto de la persona que mas se aproxima
        imageFile=open(img_path, "r")
        data = imageFile.read();
        outJson = {}
        outJson['img']=data.encode('base64')
        outJson['operation']= const.RESPONSEALREADYEXISTS
        imageFile.close()
        return jsonify(outJson);

class TrajectoryManager(Manager):

  def __init__(self, file, basedir):
    super(TrajectoryManager, self).__init__(file, basedir)

  def processRequest(self):
    if not self.fileExists:
        return jsonify(operation=const.RESPONSEDOESNTEXIST)
    img_path = self.feature_matcher.getMatch() #Deberia devolver el path de la foto de la persona que mas se aproxima
    hash_person = self.sha1.compute(img_path)
    self.cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic IN (SELECT CropFace.HashBigPic FROM CropFace WHERE CropFace.HashPerson = %s)", (hash_person,))
    rows = self.cursor.fetchall()
    if (len(rows)> 0):
        points=[]
        for current_tuple in rows:
            hash_big_pic = current_tuple[0]
            lat= current_tuple[1]
            lng= current_tuple[2]
            timestamp= current_tuple[3]
            new_json = {"lat": lat, "lng": lng}
            points.append(new_json)
    #points = [{"lat": -34.621622, "lng": -58.423759}, {"lat": -34.63186608060463, "lng": -58.42525005340576}];
    return jsonify(operation=const.RESPONSETRAJECTORY, points=json.dumps(points));

class UploadManager(Manager):

  def __init__(self, file, basedir):
    super(UploadManager, self).__init__(file, basedir)

  def processRequest(self):
    if self.fileExists:
        return self.responseAlreadyExists();
    self.file.save(os.path.join(self.updir, self.filename))
    return jsonify(operation=const.RESPONSECORRECTLYUPLOADED)

class ExistanceManager(Manager):
  def __init__(self, file, basedir):
    super(ExistanceManager, self).__init__(file, basedir)

  def processRequest(self):
    if self.fileExists:
        return self.responseAlreadyExists();
    return jsonify(operation=const.RESPONSEDOESNTEXIST)
