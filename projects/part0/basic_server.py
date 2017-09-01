import sys
import socket
import select

port = sys.argv[1]

def clientthread(conn):
    data = ''
    while data != 'exit':
        data = conn.recv(MTU)
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ('Attempting to bind')
server.bind(('127.0.0.1', int(port)))

print ('binding success!')

print ('Starting to listen')
server.listen(10)

data = ''
i = [server]

running = 1
while running:
    inputs, outputs, e = select.select(i, [], [])
    
    for s in inputs:
        if s == server:
            client, address = server.accept()
            print ('address: ' + str(address))
            inputs.append(client)
        else:
            data = s.recv(1024)
            if data:
                print (data)
            else:
                inputs.remove(s)
                s.close()
server.close() 
    
    
server.close()
sys.exit()

    