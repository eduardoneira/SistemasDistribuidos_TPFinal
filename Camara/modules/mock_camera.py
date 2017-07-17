#!/bin/python3

from modules.abstract_camera import *

class MockCamera(AbstractCamera):

  CONST_PATH_IMG_PROCESSED = './img_processed/'

  def __init__(self):
    super().__init__()

    if not os.path.exists(self.PATH_IMG_PROCESSED()):
      os.mkdir(self.PATH_IMG_PROCESSED())
    
    logging.debug('Inicializando mock camara que agarra imagenes de '+ self.PATH_IMG_PROCESSED())

  def get_frame(self):
    folder = os.listdir(self.PATH_IMG())
    img = self.INVALID()

    if folder:
      src = self.PATH_IMG()+folder[0]
      dst = self.PATH_IMG_PROCESSED()+folder[0]
      
      img = open(src,'rb')      
      img_b64 =  self.base64(img)
      img.close()

      shutil.move(src,dst)
      logging.debug('Imagen movida a procesada en '+dst)      

      return img_b64

    return img

  def PATH_IMG_PROCESSED(self):
    return self.CONST_PATH_IMG_PROCESSED