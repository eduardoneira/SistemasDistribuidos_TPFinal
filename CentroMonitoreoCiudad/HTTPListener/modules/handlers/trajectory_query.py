#!/usr/bin/python3

from modules.logger import *
from modules.db_wrapper import *
from modules.file_manager import *

class TrajectoryQuery:

  def __init__(self, db, file_manager):
    self.db = db
    self.file_manager = file_manager

  def handle(self, request, response):
    person = self.db.find_person_by_dni(request['dni'])

    if (len(person) == 0):
      response['status'] = 'NOT OK'
    else:
      big_pictures = self.db.find_big_pictures(person[0])
      if (len(big_pictures) == 0):
        response['status'] = 'NOT OK'
        response['comment'] = 'Not found yet'
      else:
        coordinates = []
        for image in big_pictures:
          big_pic_b64 =  self.file_manager.get_bigpic_base64(image[0])
          point = {"lat": image[1], "lng": image[2], 'image': big_pic_b64, "timestamp": str(image[3])}
          coordinates.append(point)

        response['coordinates'] = coordinates
        response['dni'] =  request['dni']