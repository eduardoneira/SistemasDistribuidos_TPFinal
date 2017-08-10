#!/bin/python3

import signal
import logging

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum,frame):
    self.kill_now = True
    logging.debug('Llego señal de salida. Se va a terminar la captura de fotos')
