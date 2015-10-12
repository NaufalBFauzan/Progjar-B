import socket, select

users = []
adres = []
soket = []
passw = {}
n_us  = []

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
     
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #<-
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
			if(data == 'list\n'):
				sock.send("\nSERVER:\n> list :\n")
				for i in range (len(users)):
					sock.send("- "+users[i])
					sock.send("\n")
			if(data == 'logout\n'):
				a=soket.index(sock)
				alamat=adres[a]
			        point=users[a]
			        broadcast_data(sock, "Client "+point+" is offline\n")
			        print "Client "+point+" is offline"
			        soket.remove(sock)
			        adres.remove(alamat)
				users.remove(point)				
				sock.close()
			        CONNECTION_LIST.remove(sock)
			        continue
			if(len(data) > 0) :
				data_command = data.split(' ', 1)	#<-
				if data_command[0] == "UN":
					data_user = data_command[1].split(' ', 2)
					flag=0
					for i in range (len(users)):
						if str(data_user[1]) == str(users[i]):
							flag=1
					if flag==0:
						if data_user[0] == "regist":
		   			 		adres.append(str(sock.getpeername()))
		    					users.append(str(data_user[1]))
							n_us.append(str(data_user[1]))
							passw[data_user[1]]=data_user[2]
							soket.append(sock)
							print "Client "+str(sock.getpeername())+" is successfully registered as "+str(data_user[1])
							broadcast_data(sock, str(data_user[1])+" entered room\n")
							sock.send("OK")
						if data_user[0] == "login":
							cek=0
							for i in range (len(n_us)):
								if data_user[1]==n_us[i]:
									cek=1
							if cek==0:
								print "Client "+str(sock.getpeername())+" is failed trying to loging in with username : "+str(data_user[1])
								sock.send("\rSERVER:Login failed, username didn't exist\n")
								sock.close()
				      			        CONNECTION_LIST.remove(sock)
								continue
							if data_user[2] == passw[data_user[1]] and cek==1:
								adres.append(str(sock.getpeername()))
		    						users.append(str(data_user[1]))
								soket.append(sock)
								print "Client "+str(sock.getpeername())+" is successfully loged in with "+str(data_user[1])+" as username"
								broadcast_data(sock, str(data_user[1])+" entered room\n")
								sock.send("OK")
					if flag==1:
						print "Client "+str(sock.getpeername())+" is trying using used username : "+str(data_user[1])
						sock.send("\rSERVER:Login failed, username already used by someone else\n")
						sock.close()
		      			        CONNECTION_LIST.remove(sock)
						continue
				elif data_command[0] == "sendall":
					user=users[adres.index(str(sock.getpeername()))]
		                	broadcast_data(sock, "\r" + '[' + user + '] : ' + str(data_command[1]))
				elif data_command[0] == "sendto":
					user=users[adres.index(str(sock.getpeername()))]
					data_sendto = str(data_command[1]).split(' ', 1)
					flag=0
					rece = data_sendto[0]
					for i in range (len(users)):
						if users[i]==rece:
							note=i
							flag=1
					if flag==0 :
						sock.send("SERVER: Recipient is not exist\n")						
					else:
						soket[note].send("\r" + '[' + user + '] : ' + str(data_sendto[1]))


				elif data != 'list\n':
					sock.send("\rWrong command, please try again.\nsendall [message] - to broadcast\nsendto [recipient] [message] - to direct message to certain user\nlist - to show all of active users\n")
					             
                 
                except:
			x=0
			for i in range (len(users)):
				if users[soket.index(sock)]==users[i]:
					x=1
			if(x==1) and data != 'logout\n':
			    a=soket.index(sock)
			    alamat=adres[a]
		            point=users[a]
		            broadcast_data(sock, "Client "+point+" is offline\n")
		            print "Client "+point+" is offline"
		            soket.remove(sock)
		            adres.remove(alamat)
			    users.remove(point)				
			    sock.close()
		            CONNECTION_LIST.remove(sock)
		            continue
     
    server_socket.close()
