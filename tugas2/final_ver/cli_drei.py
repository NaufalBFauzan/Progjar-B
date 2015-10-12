import socket, select, string, sys

uname = []
 
def prompt() :
    sys.stdout.write('['+u_name_+'] : ')
    sys.stdout.flush()
 
if __name__ == "__main__":
     
    host = 'localhost'
    port = 5000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    
    sys.stdout.write('Insert Username : ')
    sys.stdout.flush()
    uname = sys.stdin.readline().rstrip('\n')
    u_name = uname.split(" ",2)
    u_name_ = u_name[1]
    a = ("UN", uname)
    b = ' '
    x = b.join(a)
    s.send(x)

    flag= "OK"
    datas = s.recv(4096)
    if flag != str(datas):
	sys.stdout.write(datas)
	print "\rClient will be closed"
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
                    sys.stdout.write(data)
                    prompt()
             
            else :
                msg = sys.stdin.readline()
                s.send(msg)
		if msg == "logout\n":
			sys.exit()
                prompt()
