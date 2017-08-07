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
  def __SHA1_byte_stream(byte_stream):
    sha1 = hashlib.sha1()
    sha1.update(byte_stream.encode('utf-8'))
    return sha1.hexdigest()

  def processRequest(self):
    # points = [{"lat": -34.621622, "lng": -58.423759}, {"lat": -34.63186608060463, "lng": -58.42525005340576}];
    """file_bigpic1= "got.jpg"
    file_bigpic2= "got2.jpg"
    file_match = "jon_snow3.jpg"
    points = [{"lat": -34.621622, "lng": -58.423759, 'image':file_bigpic1}, {"lat": -34.63186608060463, "lng": -58.42525005340576, 'image':file_bigpic2}];
    json_response = jsonify(operation=CONST.RESPONSETRAJECTORY, match=file_match, points=json.dumps(points))
    return json_response"""
    response = json.loads(self.rpc_call())

    if response['status'] == 'OK':
      points = []
      image_path = "/static/images"
      image_decoded = base64.b64decode(response['bestmatch'])
      bestmatch_file_name = str(self.__SHA1_byte_stream())+".jpg"

      with open(os.path.join(image_path, bestmatch_file_name), 'wb') as file:
        file.write(image_decoded.encode('utf-8'))

      for point in response['coordinates']:
        image_decoded = base64.b64decode(point['image'])
        filename = str(self.__SHA1_byte_stream(image_decoded))+".jpg"
        #TODO: Check if it was already cached
        with open(os.path.join(image_path, filename), 'wb') as file:
          file_big_pic.write(image_decoded.encode('utf-8'))          
        points.append(point)

      jsonify(operation=CONST.RESPONSETRAJECTORY,points=json.dumps(points), match=bestmatch_file_name)
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