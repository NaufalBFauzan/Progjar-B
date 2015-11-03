import socket, select, string, sys, getpass, os
 
def prompt() :
    global uname
    sys.stdout.write('['+uname+'] : ')
    sys.stdout.flush()

def print_err(codes):
	if codes == 4011:
		print "\rSERVER : ERR4011 - Register failed, using existed username\nClient will be closed"
	elif codes == 4012:
		print "\rSERVER : ERR4012 - Login failed, username didn't exist\nClient will be closed"
	elif codes == 4001:
		print "\rSERVER : ERR4001 - Login failed, wrong password\nClient will be closed"
	elif codes == 4013:
		print "\rSERVER : ERR4013 - Login or register failed, wrong command input\nClient will be closed"
	elif codes == 4014:
		print "\rSERVER : ERR4014 - Login failed, username already used by someone else\nClient will be closed"
	elif codes == 5031:
		print "\rSERVER : ERR5031 - Failed to connect, service unavailable\nClient will be closed"
	elif codes == 4002:
		print "\rSERVER : ERR4002 - Login or register failed, wrong command input\nClient will be closed"
	elif codes == 4003:
		print "\rSERVER : ERR4003 - Login or register failed, wrong username input\nClient will be closed"
	elif codes == 4004:
		print "\rSERVER : ERR4004 - Wrong command, please try again.\nsendall [message] - to broadcast\nsendto [recipient] [message] - to direct message to certain user\nlist - to show all of active users\nlogout - to log-out and quit the chat-room"
	elif codes == 4041:
		print "\rSERVER : ERR4041 - Recipient is not exist or there is no message"

def log_reg():
    global uname
    sys.stdout.write('Register [regist] or login [login] : ')
    sys.stdout.flush()
    command1 = sys.stdin.readline().rstrip('\n')
    if (' ' in command1) == True or command1[-1]==' ' or (command1 != 'regist'):
	if(command1 != 'login'):
		print_err(int("4002"))
		sys.exit()
    sys.stdout.write('Username : ')
    uname = sys.stdin.readline().rstrip('\n')
    if (' ' in uname) == True or uname[-1]==' ':
	print_err(int("4003"))
	sys.exit()
    passwd = getpass.getpass('Password : ')
    a = ('UN', command1, uname, passwd)
    z = ' '.join(a)
    return z

if __name__ == "__main__": 
    host = 'localhost'
    port = 5000 
    global uname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2) 
    try :					#connecting socket
        s.connect((host, port))
    except :
        print_err(int("5031"))
        sys.exit()
    command=log_reg()				#getting command input for authentication
    s.send(command)
    datas = s.recv(4096)
    if int(datas) != 200:				#checking if authentication is complete or not
	print_err(int(datas))
	sys.exit()
    print 'Connected to remote host. Start sending messages'
    prompt() 
    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
		    if (data=="4004") or (data=="4041"):
			print_err(int(data))
		    else:
                    	sys.stdout.write(data)
                    prompt()
            else :
                msg = sys.stdin.readline()
		if msg != "clear\n":
			s.send(msg)
		else :
			os.system('clear')
		if msg == "logout\n":
			sys.exit()
                prompt()
