# Tcp Chat server
 
import socket, select

users = []
adres = []
soket = []
n_us  = 0
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
			if(data == 'list\n'):
				sock.send("list :\n")
				for i in range (len(users)):
					sock.send(users[i])
					sock.send("\n")
			if(len(data) > 0) :
				data_command = data.split(' ', 1)
				if data_command[0] == "UN":
					n_us=n_us+1
   			 		adres.append(str(sock.getpeername()))
    					users.append(str(data_command[1]))
					soket.append(sock)
				if data_command[0] == "sendall":
					for i in range (len(adres)):
						if adres[i]==str(sock.getpeername()):
							user=users[i]
		                	broadcast_data(sock, "\r" + '<' + user + '> ' + str(data_command[1]))
				if data_command[0] == "sendto":
					for i in range (len(adres)):
						if adres[i]==str(sock.getpeername()):
							user=users[i]
					data_sendto = str(data_command[1]).split(' ', 1)
					rece = data_sendto[0]
					for i in range (len(users)):
						if users[i]==rece:
							note=i
					soket[note].send("\r" + '<' + user + '> ' + str(data_sendto[1]))
					             
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
