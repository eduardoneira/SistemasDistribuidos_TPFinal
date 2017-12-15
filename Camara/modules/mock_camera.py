#!/bin/python3

from modules.abstract_camera import *

class MockCamera(AbstractCamera):

  CONST_PATH_IMG_PROCESSED = './img_processed/'

  def __init__(self):
    super().__init__()

    if not os.path.exists(self.PATH_IMG_PROCESSED()):
      os.mkdir(self.PATH_IMG_PROCESSED())
    
    logging.debug('Inicializando mock camara que agarra imagenes de '+ self.PATH_IMG())

  def get_frame(self):
    folder = os.listdir(self.PATH_IMG())
    img = self.INVALID()

    if folder:
      src = self.PATH_IMG()+folder[0]
      dst = self.PATH_IMG_PROCESSED()+folder[0]
      
      with open(src,'rb') as img:      
        img_b64 =  self.base64(img)

      shutil.move(src,dst)
      logging.debug('Imagen movida a procesada en '+dst)      

      return img_b64

    return img

  def close(self):
    shutil.rmtree(path = self.PATH_IMG(),
                  ignore_errors = True)

  def PATH_IMG_PROCESSED(self):
    return self.CONST_PATH_IMG_PROCESSED