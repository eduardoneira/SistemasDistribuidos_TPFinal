from flask import (
    jsonify,
    render_template
)

import os
import sys
import base64
import json
import hashlib
import pdb
sys.path.insert(0, '../')

from app_exceptions import *
from werkzeug import secure_filename
from flask_googlemaps import Map, icons

class Manager(object):
  def __init__(self, rpc_client,formData):
    self.rpc_client = rpc_client
    self.formData = formData;
    self.type = int(formData['operation']);
    self.image_list = {};
    self.image_id=0;
    self.request = {'type':self.type};
  def sha1_byte_stream(self,byte_stream):
    sha1 = hashlib.sha1(byte_stream)
    return sha1.hexdigest()
  def rpc_call(self):
    return self.rpc_client.call(json.dumps(self.request))
  def appendImage(self, file):
     image_key = "image_"+str(self.image_id);
     self.image_list[image_key] = base64.b64encode(file.read()).decode('utf-8');
     self.image_id += 1;
class TrajectoryManager(Manager):
  def __init__(self, rpc_client,formData):
    super(TrajectoryManager, self).__init__(rpc_client,formData)

  def processRequest(self):
    self.request['dni'] = int(self.formData['dni']);
    response = json.loads(self.rpc_call())
    if response['status'] == 'OK':
      points = []
      image_path = "/static/images/"

      for point in response['coordinates']:
        image_decoded = base64.b64decode(point['image'])
        filename = str(self.sha1_byte_stream(image_decoded))+".jpg"
        #TODO: Check if it was already cached
        with open('./'+image_path+filename, 'wb') as file_big_pic:
          file_big_pic.write(image_decoded)
        point['image'] = filename
        points.append(point)
      with open('./static/config.json') as config_file:
          config = json.load(config_file)
          return jsonify(operation= self.type, answer= config['RESPONSETRAJECTORY'],points=json.dumps(points))
    else:
      print(response);
      raise VoidRequest(response['comment'])

class UploadManager(Manager):
  def __init__(self,rpc_client,formData):
    super(UploadManager, self).__init__(rpc_client,formData)
    self.request['state'] = int(self.formData['state']);
    self.request['name'] = self.formData['name'];
    self.request['surname'] = self.formData['surname'];
    self.request['dni'] = int(self.formData['dni']);
  def processRequest(self):
    self.request['images'] = self.image_list;
    response = json.loads(self.rpc_call())

    if response['status'] == 'OK':
        with open('./static/config.json') as config_file:
          config = json.load(config_file)
          return jsonify(operation=self.type, answer= config['RESPONSECORRECTLYUPLOADED'])
    else:
      raise VoidRequest("Already exists")
class ExistanceManager(Manager):
  def __init__(self, rpc_client,formData):
    super(ExistanceManager, self).__init__(rpc_client,formData)

  def processRequest(self):
    self.request['images'] = self.image_list;
    response = json.loads(self.rpc_call())
    with open('./static/config.json') as config_file:
       config = json.load(config_file)
       if response['status'] == 'OK':
          #TODO: Show best match
          return jsonify(operation=self.type, answer= config['RESPONSEALREADYEXISTS'], name= response['name'], surname= response['surname'], dni= response['dni'], state= response['state'])
       else:
          raise VoidRequest("non-existent")
