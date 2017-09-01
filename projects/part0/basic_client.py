import sys
import socket
from sys import stdin

ip = sys.argv[1]
port = sys.argv[2]

print ('IP: ' + ip +'port: ' + port )

message = ''

while message != 'exit':
    message = stdin.readline()
    print ('\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send(message)
    s.close()
    
s.close()
sys.exit()
    