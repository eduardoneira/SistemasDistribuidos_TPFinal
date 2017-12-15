#!/usr/bin/python3

from modules.logger import *
from modules.face_cropper import *
from modules.db_wrapper import *
from modules.matcher_wrapper import *
from modules.file_manager import *

class UploadQuery:

  def __init__(self, db, file_manager, matcher_wrapper, cropper, missing_id):
    self.db = db
    self.matcher_wrapper = matcher_wrapper
    self.cropper = cropper
    self.file_manager = file_manager
    self.MISSING = missing_id

  def handle(self, request, response):
    if (request['state'] == self.MISSING):
      state = 'missing'
    else:
      state = 'legal_problems'

    self.db.save_person(request['dni'],
                        state,
                        request['name'],    
                        request['surname'])    
    
    response['id'] = self.db.find_person_by_dni(request['dni'])[0]
    
    for key, image in request['images'].items():
      cropped = self.cropper.crop_base64(image)[0]

      image_id = self.file_manager.save_person_base64(response['id'],
                                                      cropped)
      
      self.db.save_person_image(image_id,
                                response['id'])

      self.matcher_wrapper.dump_keypoints(image_id,
                                          cropped)