import psycopg2
import os
def startServer(execute_server_command):
    pid = os.fork()
    if pid == 0:
        os.system(execute_server_command)
        s._exit(0)
    return pid;
def main():
    #crear predictor
    pid_web_server= startServer("./ProcesadorDeImagenes/HTTP_query_handler.py 1")
    pid_common_server= startServer("./ProcesadorDeImagenes/image_listener.py 1")
    user_input = '0'
    while not user_input == 'q':
        user_input = input("Ingrese q para terminar:")
    os.kill(pid_web_server, signal.SIGINT)
    os.kill(pid_common_server, signal.SIGINT)
    os.waitpid(pid_web_server, 0)
    os.waitpid(pid_common_server,0)
if __name__ == '__main__':
    main()
