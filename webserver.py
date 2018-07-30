import socket
import threading
import sys
import os
import datetime
import logging
import time

# Config File Name
config = "ws.conf"
# Dictionary for storing all config values
settings = {}

logging.basicConfig(filename="log_webserver.txt", level=logging.DEBUG, format='%(message)s')


# Server Class
class Server:
    def __init__(self):
        self.size = 65535
        self.threads = []
        self.host = "127.0.0.1"
        self.port = 7777

    def get_config_file_data(self):
        try:
            if os.path.isfile(config):
                settings.clear()

                file_handle = open(config)
                lines = file_handle.read().splitlines()

                for line in lines:
                    if line == "" or line.split()[0] == "###":
                        continue
                    elif line.split()[0] == "Host":
                        (key, value) = line.split()
                        self.host = value
                    elif line.split()[0] == "ListenPort":
                        (key, value) = line.split()
                        self.port = int(value)
                        if int(value) < 1025 or int(value) > self.size:
                            logging.debug("Please set port no between 1025 and 65535 inclusive.")
                            print("Please set port no between 1025 and 65535 inclusive.")
                            sys.exit()
                    elif line.split()[0] == "DocumentRoot":
                        (key, value) = line.split()
                        settings[key] = value[1:-1]
                    elif line.split()[0] == "DirectoryIndex":
                        (key, value) = line.split()
                        settings[key] = value
                    elif line.split()[0] == "ContentType":
                        (key, value1, value2) = line.split()
                        settings[key + " " + value1] = value2
                    elif line.split()[0] == "KeepaliveTime":
                        (key, value) = line.split()
                        settings[key] = value
                    elif line.split()[0] == "RequestMethods":
                        (key, value) = line.split()
                        settings[key] = value.split()
                    elif line.split()[0] == "HTTPType":
                        (key, value) = line.split()
                        settings[key] = value.split()
                    else:
                        continue

                if bool(settings):
                    msg = ""
                else:
                    msg = "Configuration file not found (Dict not found)."
            else:
                msg = "Configuration file not found."
            return msg
        except IndexError:
            msg = "Please check configuration file (Index Error)."
            return msg
        except ValueError:
            msg = "Please check configuration file (Value Error)."
            return msg

    def create_socket(self):
        try:
            # Create an INET, STREAM socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Use different port if the port is in use
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # bind the socket to a host, and a port
            sock.bind((self.host, self.port))
            # queue up as many as 20 connect requests
            sock.listen(20)
            self.sock = sock
            logging.debug("Listening on Port " + str(self.port) + "...")
            print("Listening on Port " + str(self.port) + "...")
            # Call process function
            self.process()
        except socket.error as msg:
            if self.sock:
                self.sock.close()
            logging.debug("Could not open socket: " + str(msg))
            print("Could not open socket: " + str(msg))
            sys.exit(1)
        except KeyboardInterrupt:
            logging.debug("Closing Socket gracefully")
            print("Closing Socket gracefully")
            sys.exit(0)

    def file_type(self, http, ext, length):
        error = 0
        logging.debug("Extension: " + str(ext))
        # print("Extension: " + str(ext))
        if ext == "html":
            http_response = http + ' 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "htm":
            http_response = http + ' 200 OK\r\nContent-Type: text/htm\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "txt":
            http_response = http + ' 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "png":
            http_response = http + ' 200 OK\r\nContent-Type: image/png\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "gif":
            http_response = http + ' 200 OK\r\nContent-Type: image/gif\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "jpg":
            http_response = http + ' 200 OK\r\nContent-Type: image/jpg\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "jpeg":
            http_response = http + ' 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: ' + length + '\r\n\r\nConnection: close\r\n\r\n'
        elif ext == "css":
            http_response = http + ' 200 OK\r\nContent-Type: text/css\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "js":
            http_response = http + ' 200 OK\r\nContent-Type: application/javascript\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "pdf":
            http_response = http + ' 200 OK\r\nContent-Type: application/pdf\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        elif ext == "exe":
            http_response = http + ' 200 OK\r\nContent-Type: application/exe\r\nContent-Length: ' + length + '\r\nConnection: close\r\n\r\n'
        else:
            http_response = "Sending Back \r\n\r\n"
            logging.debug("File format doesn't support.")
            print("File format doesn't support.")
            error = 1

        return http_response, error

    def process(self):
        thread_count = 1
        while True:
            logging.debug("\n================== Send Other Request ========================")
            print("\n================== Send Other Request ========================")
            # Accept request
            conn, addr = self.sock.accept()
            self.conn = conn
            self.addr = addr
            logging.debug("Connection: " + str(conn))
            # print("Connection: " + str(conn))
            if conn:
                thread = MultipleThread(conn, addr, thread_count)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)
                dtime = datetime.datetime.now()
                logging.debug("\nThread:" + str(thread_count) + " Start Time: " + str(dtime))
                print("\nThread:" + str(thread_count) + " Start Time: " + str(dtime))
                thread.join()
                logging.debug("Thread:" + str(thread_count) + " Is Alive: " + str(thread.isAlive()))
                # print("Thread:" + str(thread_count) + " Is Alive: " + str(thread.isAlive()))
                dtime = datetime.datetime.now()
                logging.debug("Thread:" + str(thread_count) + " Close Time: " + str(dtime))
                print("Thread:" + str(thread_count) + " Close Time: " + str(dtime))
                thread_count = thread_count + 1
            else:
                conn.close()
                break

    def error400(self, error):
        http_response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\nContent-Length: 300\r\n\r\n"
        if error == "method":
            logging.debug("400 Error - Method")
            http_response += "<html><body><h2>400 Bad Request</h2><br />Reaseon: Invalid Method</body></html>"
        elif error == "file":
            logging.debug("400 Error - File")
            http_response += "<html><body><h2>400 Bad Request</h2><br />Reason: Invalid URL</body></html>"
        elif error == "http":
            logging.debug("400 Error - HTTP")
            http_response += "<html><body><h2>400 Bad Request</h2><br />Reason: Invalid HTTP-Version</body></html>"
        self.conn.sendall(http_response.encode())
        self.conn.close()

    def error404(self):
        logging.debug("404 Error")
        http_response = "HTTP/1.1 500 Not Found\r\nContent-Type: text/html\r\nContent-Length: 300\r\n\r\n"
        http_response += "<html><body><h2>404 Not Found</h2><br />Reason URL does not exist</body></html>"
        self.conn.sendall(http_response.encode())
        self.conn.close()

    def error500(self):
        logging.debug("500 Error")
        http_response = "HTTP/1.1 500 Internal Server Error: cannot allocate memory\r\nContent-Type: text/html\r\nContent-Length: 300\r\n\r\n"
        http_response += "<html><body><h2>500 Cannot allocate memory</h2><br /></body></html>"
        self.conn.sendall(http_response.encode())
        self.conn.close()

    def error501(self):
        logging.debug("501 Error")
        http_response = "HTTP/1.1 501 Not Implemented\r\nContent-Type: text/html\r\nContent-Length: 300\r\n\r\n"
        http_response += "<html><body><h2>501 Not Implemented</h2><br /></body></html>"
        self.conn.sendall(http_response.encode())
        self.conn.close()


# MultiThreading Class
class MultipleThread(threading.Thread):
    def __init__(self, conn, addr, thread):
        threading.Thread.__init__(self)
        self.threads = []
        self.conn = conn
        self.addr = addr
        self.thr = thread
        self.size = 65535

    def run(self):
        # del settings["RequestMethods"]
        while True:
            try:
                self.conn.settimeout(int(settings["KeepaliveTime"]))
                request = self.conn.recv(2048)

                if request:
                    method = str(request.decode().split()[0]).strip()
                    file_path = str(request.decode().split()[1]).strip()
                    http = str(request.decode().split()[2]).strip()

                    if "Connection: keep-alive" in request.decode():
                        keepalive = "Connection: keep-alive"
                    else:
                        keepalive = "Connection: close"

                    methods = settings["RequestMethods"][0].split(",")
                    httptype = settings["HTTPType"][0].split(",")

                    print("File " + str(file_path))
                    if method not in methods:
                        server.error400("method")
                        break
                    elif file_path == "":
                        server.error400("file")
                        break
                    elif http not in httptype:
                        server.error400("http")
                        break
                    elif method == "GET":
                        logging.debug("Thread:" + str(self.thr) + " Request:" + str(request))
                        logging.debug("Thread:" + str(self.thr) + " Address:" + str(self.addr))
                        print("Thread:" + str(self.thr) + " Request:" + str(request))
                        print("Thread:" + str(self.thr) + " Address:" + str(self.addr))
                        p = file_path
                        if p == "/":
                            path = settings["DocumentRoot"] + "/" + settings["DirectoryIndex"]
                            file_name = settings["DirectoryIndex"]
                        else:
                            path = settings["DocumentRoot"] + p
                            file_name = os.path.basename(p)
                        print("File Name: " + file_name)
                        if os.path.isfile(path):
                            length = str(os.path.getsize(path))
                            ext = str(file_name.split(".")[1])
                            response, error = server.file_type(http, ext, length)
                            resp = str(response)

                            if keepalive == "Connection: keep-alive":
                                if "Connection: close" in resp:
                                    resp = resp.replace("Connection: close", "Connection: keep-alive")
                                else:
                                    resp = response

                            http_response = resp.encode()

                            if error == 0:
                                f = open(path, "rb")
                                http_response += f.read()
                                self.conn.sendall(http_response)
                            else:
                                server.error501()
                                break
                        else:
                            server.error404()
                            break
                    elif method == "POST":
                        reqdata = request.decode('utf8').splitlines()
                        post_data = reqdata[-1:]
                        data = post_data[0]
                        post_name = data.replace("UrName=", "")
                        post_name = post_name.replace("+", " ")
                        p = file_path
                        if p == "/":
                            path = settings["DocumentRoot"] + "/" + settings["DirectoryIndex"]
                            file_name = settings["DirectoryIndex"]
                        else:
                            path = settings["DocumentRoot"] + p
                            file_name = os.path.basename(p)
                        if os.path.isfile(path):
                            length = str(os.path.getsize(path))
                            ext = str(file_name.split(".")[1])
                            response, error = server.file_type(http, ext, length)
                            http_response = response.encode()
                            if error == 0:
                                f = open(path, "r")
                                file_page = ""
                                for line in f.readlines():
                                    if "<pre></pre>" in line:
                                        line = line.replace(line, "<pre>Your Name is " + post_name + "</pre>")
                                    file_page += line

                                http_response += file_page.encode()
                            else:
                                server.error501()
                                break
                            self.conn.sendall(http_response)

                else:
                    self.conn.close()
                    logging.debug("Thread:" + str(self.thr) + " No request found")
                    print("Thread:" + str(self.thr) + " No request found")
                    break

            except socket.timeout:
                self.conn.close()
                logging.debug("Thread:" + str(self.thr) + " Timeout")
                print("Thread:" + str(self.thr) + " Timeout")
                break
            except Exception:
                server.error500()
                break


if __name__ == '__main__':
    server = Server()
    message = server.get_config_file_data()
    if str(message) == "":
        logging.debug("Webserver Started")
        server.create_socket()
    else:
        logging.debug(message)
        print(message)
