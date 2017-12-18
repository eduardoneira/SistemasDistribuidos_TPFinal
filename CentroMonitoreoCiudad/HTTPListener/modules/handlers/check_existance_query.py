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

  def handle(self, request, response):
    cropped_images = []
    images = request['images']

    for key, image in images.items():
      cropped_images.append(self.cropper.crop_base64(image)[0])

    ids = self.db.person_images()

    id = self.matcher_wrapper.find_match(cropped_images[0], ids)
    
    if id is not None:
      person = self.db.find_person_with_person_image(id)
      response['dni'] = person[1];
      response['state'] = person[2];
      response['name'] = person[3];
      response['surname'] = person[4];
    else:
      response['status'] = 'NOT OK'