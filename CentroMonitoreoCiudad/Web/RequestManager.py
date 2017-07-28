from flask import (
    jsonify,
    render_template
)

import os
import sys
import base64
sys.path.insert(0, '../../')
import Utils.const as CONST
import json
from werkzeug import secure_filename
from flask_googlemaps import Map, icons

class Manager(object):
    def __init__(self, file, basedir):
        self.file=file
        self.filename = secure_filename(file.filename)
        self.updir = os.path.join(basedir, 'upload/')
        self.filePath= os.path.join(self.updir, self.filename)
        self.fileExists = os.path.isfile(self.filePath)
    def responseAlreadyExists(self):
        #Deberia devolver el path de la foto de la persona que mas se aproxima
        image_file=open(self.filePath, "rb")
        base64_image_bytes = base64.b64encode(image_file.read())
        outJson = {}
        outJson['img']= base64_image_bytes.decode(CONST.ENCODING)
        outJson['operation']= CONST.RESPONSEALREADYEXISTS
        image_file.close()
        return jsonify(outJson);

class TrajectoryManager(Manager):

  def __init__(self, file, basedir):
    super(TrajectoryManager, self).__init__(file, basedir)

  def processRequest(self):
    if not self.fileExists:
        return jsonify(operation=CONST.RESPONSEDOESNTEXIST)
    points = [{"lat": -34.621622, "lng": -58.423759}, {"lat": -34.63186608060463, "lng": -58.42525005340576}];
    return jsonify(operation=CONST.RESPONSETRAJECTORY, points=json.dumps(points));

class UploadManager(Manager):

  def __init__(self, file, basedir):
    super(UploadManager, self).__init__(file, basedir)

  def processRequest(self):
    if self.fileExists:
        return self.responseAlreadyExists();
    self.file.save(os.path.join(self.updir, self.filename))
    return jsonify(operation=CONST.RESPONSECORRECTLYUPLOADED)

class ExistanceManager(Manager):
  def __init__(self, file, basedir):
    super(ExistanceManager, self).__init__(file, basedir)

  def processRequest(self):
    if self.fileExists:
        return self.responseAlreadyExists();
    return jsonify(operation=CONST.RESPONSEDOESNTEXIST)
