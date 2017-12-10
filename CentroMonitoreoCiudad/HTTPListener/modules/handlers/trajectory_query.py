#!/usr/bin/python3

from modules.logger import *
from modules.db_wrapper import *
from modules.file_manager import *

class TrajectoryQuery:

  def __init__(self, db, file_manager):
    self.db = db
    self.file_manager = file_manager

  def handle(request, response):
    person_id = self.db.find_person_by_dni(request['dni'])

    if (len(person_id) == 0):
      response['status'] = 'NOT OK'
    else:
      big_pictures = self.db.find_big_pictures(person_id)
      if (len(rows) == 0):
        #TODO: Change status to not found
        response['status'] = 'NOT OK'
      else:
        coordinates = []
        #TODO: Change to what it really retrives
        for image in big_pictures:
          big_pic_b64 =  self.file_manager.get_bigpic_base64(image[0])
          point = {"lat": image[1], "lng": image[2], 'image': big_pic_b64, "timestamp": str(image[3])}
          coordinates.append(point)

        response['coordinates'] = coordinates
        response['dni'] =  request['dni']