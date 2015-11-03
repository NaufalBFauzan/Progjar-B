import socket, select

users = []
adres = []
soket = []
passw = {}
n_us  = []
carr  = []

def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
		flag=0
		if soket.count(socket)==1:
			flag=1
		if flag==1:
                	socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

def rm_user(socks) :
	a=soket.index(socks)
	alamat=adres[a]
        point=users[a]
        broadcast_data(sock, "Client "+point+" is offline\n")
        print "Client "+point+" is offline"
        soket.remove(socks)
        adres.remove(alamat)
	users.remove(point)				
	socks.close()
        CONNECTION_LIST.remove(socks)

def user_log(socks, usname, condition) :
	adres.append(str(socks.getpeername()))
	users.append(str(usname))
	soket.append(socks)
	if condition == 'regist':
		print "Client "+str(socks.getpeername())+" is successfully registered as "+str(usname)
	else :
		print "Client "+str(sock.getpeername())+" is successfully loged in with "+str(data_user[1])+" as username"
	broadcast_data(sock, str(usname)+" entered room\n")
	socks.send("200")

def error_log(condition, socks, route) :
	if route==1 :
		if condition==1 :
			print "Client "+str(sock.getpeername())+" is trying to register using existed username"
			sock.send("4011")
		elif condition==2 :
			print "Client "+str(sock.getpeername())+" is failed trying to loging in with username : "+str(data_user[1])
			sock.send("4012")
		elif condition==3 :
			print "Client "+str(sock.getpeername())+" is failed trying to loging in with username : "+str(data_user[1])
			sock.send("4001")
		elif condition==4 :
			print "Client "+str(sock.getpeername())+" is using wrong log-in or register command"
			sock.send("4013")	
		elif condition==5 :
			print "Client "+str(sock.getpeername())+" is trying using used username : "+str(data_user[1])
			sock.send("4014")
		socks.close()
		CONNECTION_LIST.remove(socks)
	elif route==0 :
		if condition==1 :
			sock.send("4004")
		if condition==2 :
			sock.send("4041")
		

def interaction(socks, command, message) :
	user=users[adres.index(str(socks.getpeername()))]
	if command == 'sendall' and len(message) != 0: 
		broadcast_data(socks, "\r" + '[' + user + '] : ' + str(message))
	elif command == 'sendto': 
		data_sendto = str(message).split(' ', 1)
		flag=0
		rece = data_sendto[0]
		if users.count(rece)==1:
			flag=1
		if flag==0 :
			error_log(2, socks, 0)				
		else:
			for i in range (len(users)):
				if users[i]==rece:
					note=i
			soket[note].send("\r" + '[' + user + '] : ' + str(data_sendto[1]))
	else :
		error_log(1, socks, 0)

if __name__ == "__main__":
     
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
			data_command = data.split(' ', 1)
			if(data == 'list\n'):
				carr.append("\nSERVER:\n> list :\n")
				for i in range (len(users)):
					carr.append("- "+users[i]+"\n")
				sock.send(' '.join(carr))
				del carr
			elif(data == 'logout\n'):
				rm_user(sock)
			        continue	
			elif data_command[0] == "UN":
				data_user = data_command[1].split(' ', 2)
				flag=0
				if users.count(data_user[1])==1:
					flag=1
				if flag==0:
					if data_user[0] == "regist":
						flags=0
						if n_us.count(data_user[1])==1:
							flags=1
						if flags==0:
							n_us.append(str(data_user[1]))
							passw[data_user[1]]=data_user[2]
		   			 		user_log(sock, data_user[1], "regist")
						elif flags==1:
							error_log(1, sock, 1)
							continue
					elif data_user[0] == "login":
						cek=0
						if n_us.count(data_user[1])==1:
							cek=1
						if cek==0:
							error_log(2, sock, 1)
							continue
						if data_user[2] == passw[data_user[1]] and cek==1:
							user_log(sock, data_user[1], "login")
						elif cek==1 and data_user[2] != passw[data_user[1]]:
							error_log(3, sock, 1)
							continue
					else:
						error_log(4, sock, 1)
						continue
				if flag==1:
					error_log(5, sock, 1)
					continue
			elif data_command[0]=="sendall" or data_command[0]=="sendto" :
				interaction(sock, data_command[0], data_command[-1])
			else :
				error_log(1, sock, 0)
                except:
			x=0
			for i in range (len(users)):
				if users[soket.index(sock)]==users[i]:
					x=1
			if(x==1) and data != 'logout\n':
			    rm_user(sock)
		            continue
     
    server_socket.close()
