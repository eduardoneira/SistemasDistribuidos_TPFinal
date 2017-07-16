#!/bin/python3

from camera import *

class RealCamera(AbstractCamara):

  CONST_PATH_IMG_PROCESSED = './img_processed/'

  def __init__(self):
    super().__init__()
    
    logging.debug('Inicializando mock camara que agarra imagenes de '+ PATH_IMG_PROCESSED())

  def get_frame(self):
    folder = os.listdir(PATH_IMG())
    img = INVALID()

    if not folder
      
      img = open(PATH_IMG()+folder[0],'rb')
      logging.debug('Moviendo imagen a procesada en '+PATH_IMG_PROCESSED()+filename)
      
      return base64(img)

    return img

  def PATH_IMG_PROCESSED:
    return CONST_PATH_IMG_PROCESSED