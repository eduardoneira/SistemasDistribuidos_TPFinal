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

  def processRequest(self):
    # points = [{"lat": -34.621622, "lng": -58.423759}, {"lat": -34.63186608060463, "lng": -58.42525005340576}];
    file_bigpic1= "got.jpg"
    file_bigpic2= "got2.jpg"
    file_match = "jon_snow3.jpg"
    points = [{"lat": -34.621622, "lng": -58.423759, 'image':file_bigpic1}, {"lat": -34.63186608060463, "lng": -58.42525005340576, 'image':file_bigpic2}];
    json_response = jsonify(operation=CONST.RESPONSETRAJECTORY, match=file_match, points=json.dumps(points))
    return json_response
    """response = json.loads(self.rpc_call())

    if response.status == 'OK':
      points =[]
      for p in response.coordinates:
        points.append({ 'lat':p[0],'lng':p[1] })
      jsonify(operation=CONST.RESPONSETRAJECTORY,points=json.dumps(points))
    else:
      return jsonify(operation=CONST.RESPONSEDOESNTEXIST, points="");"""

class UploadManager(Manager):
  def __init__(self, file,rpc_client,type,state):
    super(UploadManager, self).__init__(file,rpc_client,type)
    self.request['state'] = state

  def processRequest(self):
    response = json.loads(self.rpc_call())

    if response.status == 'OK':
      return jsonify(operation=CONST.RESPONSECORRECTLYUPLOADED)

class ExistanceManager(Manager):
  def __init__(self, file,rpc_client,type):
    super(ExistanceManager, self).__init__(file,rpc_client,type)

  def processRequest(self):
    response = json.loads(self.rpc_call())

    if response.status == 'OK' and response['found']:
      return jsonify(operation=CONST.RESPONSEALREADYEXISTS)
    else:
      return jsonify(operation=CONST.RESPONSEDOESNTEXIST)
