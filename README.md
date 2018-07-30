# HTTP_based_web_server
HTTP-based web server that handles multiple simultaneous requests from users.

---------------------------------------------------------------------------------------------------
Objective:
---------------------------------------------------------------------------------------------------
Create HTTP-based web server
Handles multiple simultaneous requests from users

---------------------------------------------------------------------------------------------------
Background:
---------------------------------------------------------------------------------------------------
Basics of Socket programming for TCP connections.
Handle multiple request.
Handling errors in the code.
Logging the file instead of printing.

---------------------------------------------------------------------------------------------------
Implementation:
---------------------------------------------------------------------------------------------------
Implementation Details
Read config file and get all the details in dictionary which is global.
If there is error the program will exit.
If the port no mentioned in the program is invalid or less than 1024 then the program will exit.

Multithreading is used for handling the request.
For each port multiple thread will be opened and in the single connection all the files will be fetched.
If there is timeout, the new connection will be opened with different port no and the remaining files 
will be fetched.


If there is error then they are handled by one of the following error handling request:
HTTP 400 Error
If the path is invalid, then the error will be handled by error400 function.
If the http version is other than HTTP1.0, HTTP1.1, then the error will be handled by error400 function.

HTTP 404 Error
If the file is not found in the document_root_directory folder, then the error will be handled by error404 function.

HTTP 500 Error
If there is error in config file, then the error will be handled by error500 function

HTTP 501 Error
If the method is used different other than GET, POST, then the error will be handled by error501 function.
If the valid content type is not present in the confg file, then the error will be handled by error501 function.


Client:
Run the client file.
The client should request first 100 different files to the server and then request same file 100 times
to the server.
If the file is present, the the 200 OK response will be send by the server.
If it is not present, then the respective error will be handled by the server.

cleintfile.py:
clientfile.py file is used for creating files for testing.

---------------------------------------------------------------------------------------------------
Requirement:
---------------------------------------------------------------------------------------------------
Python v3.6.2

Inside document_root_directory folder there are multiple files.
For Demo test site: testsite  which contains many files for that site
For Server: webserver.py
For Client: client.py
For configuration file: ws.conf
For creating 100 files: createfile.py

Log files will be created for client and webserver
client: 	log_client.txt
webserver: 	log_webserver.txt

---------------------------------------------------------------------------------------------------
Folder Hierarchy:
---------------------------------------------------------------------------------------------------
All files will be in document_root_directory group based upon their file type.

---------------------------------------------------------------------------------------------------
IDE for Development:
---------------------------------------------------------------------------------------------------
Pycharm
Terminal window inside pycharm for running program.

---------------------------------------------------------------------------------------------------
Instruction for running program:
---------------------------------------------------------------------------------------------------
Server 
webserver.py

Client
client.py

---------------------------------------------------------------------------------------------------
