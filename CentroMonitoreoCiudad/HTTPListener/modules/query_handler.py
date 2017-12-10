#!/usr/bin/python3

from modules.handlers.upload_query import *
from modules.handlers.check_existance_query import *
from modules.handlers.trajectory_query import *

class QueryHandler:
  
  def __init__(self, config):
    self.cropper = FaceCropper(config['face_cropper'])
    self.file_manager = FileManager(config['filesystem'])
    self.matcher_wrapper = MatcherWrapper(config['matcher'], self.file_manager)
    self.db = DBWrapper(config['db'])
    self.__create_handlers(config['requests'])

  def __create_handlers(self, config):
    self.handlers = {}
    self.handlers[config['existance']] = CheckExistanceQuery(self.db,
                                                             self.matcher_wrapper,
                                                             self.cropper)
    
    self.handlers[config['upload']] = UploadQuery(self.db,
                                                  self.file_manager,
                                                  self.matcher_wrapper,
                                                  self.cropper,
                                                  config['missing'])
  
    self.handlers[config['trajectory']] = TrajectoryQuery(self.db,
                                                          self.file_manager,
                                                          self.cropper)

  def handle(body):
    request = json.loads(body.decode('utf-8'))
    response = {}
    response['status'] = 'OK'
    
    try:
      logging.debug("Llego una request de tipo "+ request['type'])
      handlers[int(request['type'])].handle(request, response)
    except KeyError:
      response['status'] = 'ERROR'
      response['message'] = 'Tipo de mensaje invalido'
    
    return json.dumps(response)
  
  def close(self):
    self.db.close()
