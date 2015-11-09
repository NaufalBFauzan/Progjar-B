import sys
import socket
import re
import threading
import time

def get_file(nama):
	myfile = open(nama)
	return myfile.read()

hateemel = """HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Success nyaa~ :3</title>
</head>
<body>
Wrong Adress it seems, you can try link bellow :<br>
<a href='http://localhost:3175/gambar1'>'gambar 1'</a><br>
<a href='http://localhost:3175/gambar2'>'gambar 2'</a><br> 
<a href='http://localhost:3175/gambar3'>'gambar 3'</a><br> 
<a href='http://localhost:3175/gambar4'>'gambar 4'</a><br> 
<a href='http://localhost:3175/gambar5'>'gambar 5'</a><br> 
</body>
</html>
"""

class clients_process(threading.Thread):
	def __init__(self,connection,client_address):
		self.connection=connection
		self.client_address=client_address
		threading.Thread.__init__(self)

	def run(self):
		message=''
		while True:
			data=self.connection.recv(1024)
			if data:
				message=message+data
				match = re.match('GET /gambar(\d+)\sHTTP/1', message)
				if match:
					ID = match.group(1)
					if int(ID)==1:
						self.connection.send(get_file('gambar1.jpg'))
					elif int(ID)==2:
						self.connection.send(get_file('gambar2.jpg'))
					elif int(ID)==3:
						self.connection.send(get_file('gambar3.jpg'))
					elif int(ID)==4:
						self.connection.send(get_file('gambar4.jpg'))
					elif int(ID)==5:
						self.connection.send(get_file('gambar5.jpg'))
				else :
					self.connection.send(hateemel)
			self.connection.close()
			break




class server(threading.Thread):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost', 3175)
		self.sock.bind(self.server_address)
		threading.Thread.__init__(self)
		
	def run(self):
		self.sock.listen(1)
		while True:
			self.connection, self.client_address = self.sock.accept()
			mein_client=clients_process(self.connection, self.client_address)
			mein_client.start()


if __name__ == "__main__":
	mein_server = server()
	mein_server.start()
