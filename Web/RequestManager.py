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
import Utils.const as CONST

from werkzeug import secure_filename
from flask_googlemaps import Map, icons

class Manager(object):
  def __init__(self,file,rpc_client,type):
    self.file=file
    self.rpc_client = rpc_client
    self.type = type
    self.request = {'type':self.type,
                    'image':base64.b64encode(self.file.read()).decode('utf-8')}
  def rpc_call(self):
    return self.rpc_client.call(json.dumps(self.request))

class TrajectoryManager(Manager):
  def __init__(self, file,rpc_client,type):
    super(TrajectoryManager, self).__init__(file,rpc_client,type)
  
  def __SHA1_byte_stream(self,byte_stream):
    sha1 = hashlib.sha1(byte_stream)
    return sha1.hexdigest()

  def processRequest(self):
    response = json.loads(self.rpc_call())

    # pdb.set_trace()

    if response['status'] == 'OK':
      points = []
      image_path = "/static/images/"
      image_decoded = base64.b64decode(response['bestmatch'])
      bestmatch_file_name = str(self.__SHA1_byte_stream(image_decoded))+".jpg"

      with open('./'+image_path+bestmatch_file_name, 'wb') as file:
        file.write(image_decoded)

      for point in response['coordinates']:
        image_decoded = base64.b64decode(point['image'])
        filename = str(self.__SHA1_byte_stream(image_decoded))+".jpg"
        #TODO: Check if it was already cached
        with open('./'+image_path+filename, 'wb') as file:
          file_big_pic.write(image_decoded)          
        points.append(point)

      # pdb.set_trace()

      return jsonify(operation=CONST.RESPONSETRAJECTORY,points=json.dumps(points), match=bestmatch_file_name)
    else:
      return jsonify(operation=CONST.RESPONSEDOESNTEXIST, points="");

class UploadManager(Manager):
  def __init__(self,file,rpc_client,type,state):
    super(UploadManager, self).__init__(file,rpc_client,type)
    self.request['state'] = state

  def processRequest(self):
    response = json.loads(self.rpc_call())

    if response['status'] == 'OK':
      return jsonify(operation=CONST.RESPONSECORRECTLYUPLOADED)

class ExistanceManager(Manager):
  def __init__(self, file,rpc_client,type):
    super(ExistanceManager, self).__init__(file,rpc_client,type)

  def processRequest(self):
    response = json.loads(self.rpc_call())

    if response['status'] == 'OK' and response['found']:
      #TODO: Show best match
      return jsonify(operation=CONST.RESPONSEALREADYEXISTS)
    else:
      return jsonify(operation=CONST.RESPONSEDOESNTEXIST)