#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        dataString = self.data.decode('utf-8').split('\r\n')

        if dataString == ['']:
            return
        # get the request method
        splitData = dataString[0].split(' ')
        method = splitData[0]
        # get the request path
        path = splitData[1]

        # check if the request method is GET
        if method != 'GET':
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return
        
        # check if the request path is valid
        try:
            filePath = './www'+path

            if ('../' in path):
                dotCounter = 0
                valCounter = 0

                for i in path.split('/'):
                    if i == '..':
                        dotCounter += 1
                    else:
                        valCounter += 1
                if dotCounter >= valCounter:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                    return
            
            # check if the request path is a directory
            if os.path.isdir(filePath):

                f = open(filePath+'/index.html', 'r')
                content = f.read()
                if path[-1] != '/':
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))
                    self.request.sendall(bytearray("Location: "+path+"/\r\n",'utf-8'))
                    f.close()
                    return

                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/html\r\n",'utf-8'))
                self.request.sendall(bytearray(content+'\r\n','utf-8'))
                f.close()
                return

            f = open(filePath, 'r')
            content = f.read()
            # check if the request path is a html file
            if path[-5:] == '.html':
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/html\r\n",'utf-8'))
                self.request.sendall(bytearray(content+'\r\n','utf-8'))
                f.close()
                return
            
            # check if the request path is a css file
            elif path[-4:] == '.css':
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/css\r\n",'utf-8'))
                self.request.sendall(bytearray(content+'\r\n','utf-8'))
                f.close()
                return

            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                f.close()
                return

        except:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
