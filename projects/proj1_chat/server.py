import sys
import socket
import select
import utils

class Channel:
    def __init__(self):
        self.channel_lst = {} #list of name
        self.session_to_channel = {}
        
    def create(self, name, s):
        newgroup = Group(name)
        self.channel_lst[name] = newgroup
        self.session_to_channel[s] = name
        
    def shchannel(self):
        for i in self.channel_lst:
            sys.stdout.write(i)
            
    def multicast(self, group, msg):
        self.channel_lst[group].boardcast(msg)
        

class Group:
    def __init__(self, x):
        self.name = x
        self.member = []
        
    def join_member(self, s):
        self.member.append(s.socket)
        
    def drop_member(self, s):
        self.member.remove(s.socket)
        
    def boardcast(self, msg):
        for i in self.member:
            i.send(msg)
            
    
class Session:
    def __init__(self, s):
        self.socket = s

port = sys.argv[1]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('127.0.0.1', int(port)))
print ('binding success!')

server.listen(10)
print ('Starting to listen')

data = ''
inputs = [server]
outputs = []
MTU = 200

running = 1

server_channel = Channel()

def is_command(x, s):
    if (' ' in x):
        if x.split(' ')[1] == "/list\n":
            server_channel.shchannel()
            
        elif x.split(' ')[1].startswith('/create '):
            server_channel.create(x.split(' ')[2], s) #channel name
            
            
        elif x.split(' ')[1].startswith('/join '):
            channel_name = x.split(' ')[2]
            if channel_name in server_channel.channel_lst:
                if s in server_channel.session_to_channel:
                    server_channel.channel_lst[server_channel.session_to_channel[s]].drop_member(s)
                else:
                    server_channel.session_to_channel[s] = channel_name
                    server_channel.channel_lst[channel_name].join_member(s)
            else:
                print (utils.SERVER_NO_CHANNEL_EXISTS)
            

while running:
    input_stream, output_stream, e = select.select(inputs, outputs, [1])
    
    for s in input_stream: #inbround traffic
        if s is server:
            client, client_address = s.accept()
            
            print ('Client connected [address]: ' + str(client_address))
    
            connection = Session(client)
            
            print('Session has been added')
            inputs.append(client)
            
        else:
            print('pending to receive')
            data = s.recv(MTU)
            data = data.rstrip(' ')
            if data:
                is_command(data, s)
                print (data)
                print('finished receive')
            else:
                inputs.remove(s)
                
    # for s in output_stream: #outbround traffic
    #     s.send(data)
    
    for s in e:
        inputs.remove(s)
        s.close()
        
server.close() 

sys.exit()

    