#!/usr/bin/python3

from modules.logger import *
from modules.matcher_wrapper import *
from modules.face_cropper import *
from modules.db_wrapper import *

class CheckExistanceQuery:

  def __init__(self, db, matcher_wrapper, cropper):
    self.db = db
    self.matcher_wrapper = matcher_wrapper
    self.cropper = cropper

  def handle(request, response):
    cropped_images = []
    images = request['images']

    for key, image in images.items():
      cropped_images.append(cropper.crop_base_64(image)[0])

    ids = self.db.most_wanted_people()
    #TODO: Adapt to multiple, change must be in matcher wrapper
    id = self.matcher_wrapper.find_match(cropped_images[0], ids)
    
    if id is not None:
      person = db.find_person()
      response['dni'] = rows[1];
      response['state'] = rows[2];
      response['name'] = rows[3];
      response['surname'] = rows[4];
    else:
      response['status'] = 'NOT OK'