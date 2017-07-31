from multiprocessing import Process
from ProcesadorDeImagenes.image_listener import image_listener_start
from ProcesadorDeImagenes.HTTP_query_handler import HTTP_query_handler_start
import os
import signal
import sys
sys.path.insert(0, '../')
import Utils.const as CONST
def main():
    #crear predictor
    """paths = [CONST.PERSONIMAGECONTAINERFOLDER, CONST.PERSONIMAGECONTAINERFOLDER, CONST.BIGPICIMAGECONTAINERFOLDER]
    for current_path in paths:
        if not os.path.exists(current_path):
            os.makedirs(current_path)"""
    http_query_handler_process = Process(target=HTTP_query_handler_start)
    image_listener_process = Process(target= image_listener_start)
    http_query_handler_process.start()
    image_listener_process.start()
    user_input = '0'
    while not user_input == 'q':
        user_input = input("Ingrese q para terminar:")
    http_query_handler_process.terminate()
    #image_listener_process.terminate()
    os.kill(image_listener_process.pid, signal.SIGINT)
    http_query_handler_process.join()
    image_listener_process.join()
if __name__ == '__main__':
main()