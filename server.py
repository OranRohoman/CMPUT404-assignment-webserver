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
# Sources:
# Ma0:    https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python 
# https://docs.python.org/2/library/os.html#os.listdir0
# https://docs.python.org/3/library/os.path.html
# guru99:    https://www.guru99.com/python-check-if-file-exists.html


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print(self.data)
        
        args =  self.data.decode().split(" ")
        #print(args)
        self.method = args[0]
        self.http = "HTTP/1.1 "
        self.status_code = ""
        self.content_type = ""
        self.content = ""
        if(len(args)>1):
            self.directory = args[1]

        if(self.method == "GET"):
            self.status_code,self.content_type,self.content = self.check_dir()
            self.actual_response = self.http + self.status_code + self.content_type + self.content
           
            self.request.sendall(self.actual_response.encode())
        else:
            self.actual_response = self.http + "405 Method Not Allowed" +"\r\n Content-Type: text/html\r\n"+"405 Method Not Allowed"+"\r\n\r\n"
            self.request.sendall(self.actual_response.encode())

       
    def check_dir(self):
        #handle base dir or /index.html
        path,req_file = os.path.split(self.directory)
        nonsense = path.split("/")
       
        if(path == "/"):
            #redirect
            if(os.path.isdir("www/"+req_file) and len(req_file) > 0):
                quicky_html = '''
                <DOCTYPE! html>
                <html>
                <body>
                <b>WRONG URL SILLY</b>
                 
                <a href="'''+req_file+'''/index.html">you want whats here</a>
                </body>
                </html>
                '''
                return "301 Moved Permanently\r\n","Content-Type: text/html\r\n\n" ,quicky_html+ "\r\n\r\n"
            #proper path
            elif(req_file == ""):
                for file in os.listdir("www/"+path):
                    if(file.endswith(".html")):
                        name = os.fsdecode(file)
                        #print(name)
                        data = open("www/"+path+"/"+name,"r").read()
                        return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"
            elif(req_file == "index.html"):
                data = open("www/index.html","r").read()
                return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"
            #css files
            elif(".css" in req_file and os.path.exists("www/"+req_file)):
                data = open("www/"+req_file,"r").read()
                return "200 OK\r\n","Content-Type: text/css\r\n\n",data+"\r\n\r\n"
            #404
            else:
                return "404 Not found\r\n","Content-Type: text/html\r\n\n","\r\n\r\n"
        #paths that are /deep/ or /deep/...
        elif(path == "/deep"):
            #proper path
            if(req_file == "" or req_file == "index.html"):
                data = open("www/deep/index.html","r").read()
                return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"

            elif(".css" in req_file and os.path.exists("www/deep/"+req_file)):
                data = open("www/deep/"+req_file,"r").read()
                return "200 OK\r\n","Content-Type: text/css\r\n\n",data+"\r\n\r\n"
            else:
                return "404 Not found\r\n","Content-Type: text/html\r\n\n","\r\n\r\n"
        #nested edge cases (hardcore/deep, hardcore/deep/, hardcore/deep/index.html or sads.css, hardcore)
        elif(os.path.isdir("www"+path)):
            #proper nested
            if(req_file == ""):
                for file in os.listdir("www/"+path):
                    if(file.endswith(".html")):
                        name = os.fsdecode(file)
                        #print(name)
                        data = open("www/"+path+"/"+name,"r").read()
                        return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"
        
            elif(".html" in req_file):
                data = open("www"+path+"/"+req_file,"r").read()
                return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"
            elif(".css" in req_file):
                data = open("www"+path+"/"+req_file,"r").read()
                return "200 OK\r\n","Content-Type: text/css\r\n\n",data+"\r\n\r\n"
            elif(os.path.isdir("www"+path) and req_file == ""):
                for file in os.listdir("www/"+path):
                    if(file.endswith(".html")):
                        name = os.fsdecode(file)
                        #print(name)
                        data = open("www/"+nonsense[1]+"/"+name,"r").read()
                        return "200 OK\r\n","Content-Type: text/html\r\n\n",data+"\r\n\r\n"
            #redirect            
            elif(os.path.isdir("www"+path +"/"+req_file)):
                #print("entering")
                quicky_html = '''
                <DOCTYPE! html>
                <html>
                <body>
                <b>WRONG URL SILLY</b>
                 
                <a href="'''+path +"/"+req_file+'''/index.html">you want whats here</a>
                </body>
                </html>
                '''
                return "301 Moved Permanently\r\n","Content-Type: text/html\r\n\n" ,quicky_html+ "\r\n\r\n"
            else:
                return "404 Not found\r\n","Content-Type: text/html\r\n\n","\r\n\r\n"
        #404
        else:
            return "404 Not found\r\n","Content-Type: text/html\r\n\n","\r\n\r\n"
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
