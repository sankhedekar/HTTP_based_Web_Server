import socket
import threading
import logging
import datetime
import sys
import time

logging.basicConfig(filename="log_client.txt", level=logging.DEBUG, format='%(message)s')


class Client:
    def send_request(self):
        try:
            for file in range(1, 101):
                t = MultipleThread(file)
                t.setDaemon(True)
                t.start()
                s_time = datetime.datetime.now()
                logging.debug(t.start)
                logging.debug("Thread started: " + str(s_time))
                t.join()
                e_time = datetime.datetime.now()
                logging.debug("Thread ended: " + str(e_time))
                t_time = e_time - s_time
                logging.debug("Thread time: " + str(t_time) + "\n")

            for i in range(100):
                file = "1"
                t = MultipleThread(file)
                t.setDaemon(True)
                t.start()
                s_time = datetime.datetime.now()
                logging.debug(t.start)
                logging.debug("Thread started: " + str(s_time))
                t.join()
                e_time = datetime.datetime.now()
                logging.debug("Thread ended: " + str(e_time))
                t_time = e_time - s_time
                logging.debug("Thread time: " + str(t_time) + "\n")

        except Exception:
            print("Server was closed.")
            sys.exit(0)


class MultipleThread(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.threads = []
        self.host = '127.0.0.1'
        self.port = 7777
        self.size = 65535
        self.file = file

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            file = "file" + str(self.file) + ".html"
            message = "GET /files/" + str(file) + " HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
            sock.sendall(message.encode())
            print("\nFile Name: " + str(file))
            logging.debug("File Name: " + str(file))
            print("Request Message:  " + str(message.encode()))
            # time.sleep(2)
            data = sock.recv(self.size)
            print("Response Message: " + str(data))
            sock.shutdown(socket.SHUT_WR)
        except Exception as e:
            print("Server was closed.")
            sys.exit(0)


if __name__ == '__main__':
    try:
        client = Client()
        client.send_request()
    except Exception:
        print("Server was closed.")
        sys.exit(0)
