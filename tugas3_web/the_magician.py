import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 1175)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# HTML script that will sent to web browser client
hateemel = "test~ :3"

while True:
    	# Wait for a connection
    	print >>sys.stderr, 'waiting for a connection'
    	connection, client_address = sock.accept()
    	print >>sys.stderr, 'connection from', client_address
    	# Receive the data in small chunks and retransmit it
    	while True:
        	data = connection.recv(1024)
        	print >>sys.stderr, 'received "%s"' % data
            	if data:
                	print >>sys.stderr, 'sending data back to the client'
                	connection.sendall(hateemel)
			connection.close()
			break
            	else:
                	print >>sys.stderr, 'no more data from', client_address
                	break
        # Clean up the connection
	connection.close()
