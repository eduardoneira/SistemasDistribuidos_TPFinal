#!/bin/python3

from camera import *
import pygame
import pygame.camera

#TODO: TEST
class RealCamera(AbstractCamara):
  
  def __init__(self,path,resolution):
    super().__init__()
    
    pygame.camera.init()
    #pygame.camera.list_camera() #Camera detected or not
    logging.debug('Inicializando camara ubicada en '+path+'con resolucion'+str(resolution))
    self.__cam = pygame.camera.Camera(path,resolution)
    self.__cam.start()

  def get_frame(self):
    img = self.__cam.get_image()
    filename = 'img'+str(self.__id)+'.jpg'
    self.__id += 1

    pygame.image.save(img,PATH_IMG()+filename)
    logging.debug('Guardando frame en '+PATH_IMG()+filename)

    img = open(PATH_IMG()+filename,'rb')
    
    return base64(img)