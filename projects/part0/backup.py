import select
import socket
import sys
import utils

HOSTNAME = sys.argv[1]
IP = sys.argv[2]
PORT = sys.argv[3]
MTU = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP, int(PORT)))

msg_prefix = ''

i = [sys.stdin, server]

while True:
    inputs, outputs, error = select.select(i, [], [])
    for s in inputs:
        if s is server:
            msg = s.recv(MTU)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                sys.stdout.write(msg.decode())
        else:
            msg = utils.CLIENT_MESSAGE_PREFIX + ' ' + sys.stdin.readline()
            server.sendall(msg.encode())



# message = ''

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.connect((IP, int(PORT)))

# inputs = [server, sys.stdin]
# outputs = []

# while True:
#     input_stream, output_stream, exception = select.select(inputs, outputs, [])
    
#     for s in input_stream:
#         if s is server:
#             message = s.recv(MTU)
#             sys.stdout.write(message.decode())
#             message = ''
#         else:
#             sys.stdout.write(utils.CLIENT_MESSAGE_PREFIX + ' ')
#             message = stdin.readline()
#             s.sendall(("[" + HOSTNAME + "] " + message).encode())

# s.close()
