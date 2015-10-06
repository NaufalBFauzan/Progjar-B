# telnet program example
import socket, select, string, sys

uname = []
 
def prompt() :
    sys.stdout.write('<'+uname+'> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    host = 'localhost'
    port = 5000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
    
    sys.stdout.write('<Insert Username> : ')
    sys.stdout.flush()
    uname = sys.stdin.readline().rstrip('\n')
    a = ("UN", uname)
    b = ' '
    x = b.join(a)
    s.send(x)

    print 'Connected to remote host. Start sending messages'
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
		#msg = sys.stdin.readline()
		#a = ("sendall", msg)
   		#b = ' '
		#x = b.join(a)
		#s.send(x)
		#prompt()
