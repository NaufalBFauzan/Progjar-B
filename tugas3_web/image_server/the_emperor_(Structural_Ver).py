import sys
import socket
import re

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

if __name__=="__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 3175)
	sock.bind(server_address)
	sock.listen(1)

	while True:
	    	connection, client_address = sock.accept()
		while True:
			data = connection.recv(1024)
			if data:
				match = re.match('GET /gambar(\d+)\sHTTP/1', data)
				if match:
					ID = match.group(1)
					if int(ID)==1:
						connection.sendall(get_file('gambar1.jpg'))
					elif int(ID)==2:
						connection.sendall(get_file('gambar2.jpg'))
					elif int(ID)==3:
						connection.sendall(get_file('gambar3.jpg'))
					elif int(ID)==4:
						connection.sendall(get_file('gambar4.jpg'))
					elif int(ID)==5:
						connection.sendall(get_file('gambar5.jpg'))
				else :
					connection.sendall(hateemel)
			connection.close()
			break
