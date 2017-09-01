import select
import socket
import sys
import utils

HOSTNAME = sys.argv[1]
IP = sys.argv[2]
PORT = sys.argv[3]
MTU = 200

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, int(PORT)))

socket_list = [sys.stdin, client]

sys.stdout.write (utils.CLIENT_MESSAGE_PREFIX + ' ')
sys.stdout.flush()

while True:
    inputs, outputs, exception = select.select(socket_list, [], [])
    for s in inputs:
        if s is client:
            msg = s.recv(MTU)
            if not msg:
                print("Connection Timeout")
            else:
                if not msg.startswith('[' + HOSTNAME + '] '):
                    sys.stdout.write(msg.decode())
        else:
            data = sys.stdin.readline()
            
            msg = '[' + HOSTNAME +'] ' + data
            print (len(msg))
            pad_time = 200 - len(msg)
            msg = msg.ljust(pad_time)
            client.sendall(msg.encode())
            sys.stdout.write (utils.CLIENT_MESSAGE_PREFIX + ' ')
            sys.stdout.flush()
            

