from Block import *
import socket 
from threading import Thread 
from socketserver import ThreadingMixIn
from os import path
import json
from Blockchain import *
import json

running = True
global blockchain
blockchain = Blockchain()

def startApplicationServer():
    class ClientThread(Thread): 
 
        def __init__(self,ip,port): 
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port 
            print('Request received from Client IP : '+ip+' with port no : '+str(port)+"\n") 
 
        def run(self): 
            data = conn.recv(10000)
            data = json.loads(data.decode())
            request_type = str(data.get("type"))
            if request_type == 'get':
                data = str(data.get("data"))
                data = int(data)
                b = blockchain.chain[data]
                data = b.transactions
                data = data[0]
                conn.send(data.get("Blockdata").encode())
            if request_type == 'store':
                data = str(data.get("data"))
                x =  '{ "Blockdata":"'+data+'"}'
                blockchain.add_new_transaction(json.loads(x))
                hash = blockchain.mine()
                for i in range(len(blockchain.chain)):
                    b = blockchain.chain[i]
                    data = b.transactions
                    print("===============================================================================================")
                    print("Block No : "+str(b.index))
                    print("Block Chain Data : "+str(data))
                    print("Previous Block Hash : "+str(b.previous_hash))
                    print("Current Block Hash : "+str(b.hash))
                    print("Verification Successfull")
                    print("===============================================================================================\n")
                conn.send(str('Node1 received blockchain transaction').encode())
            
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('localhost', 3333))
    threads = []
    print("Blockchain node2 Started & waiting for incoming connections\n")
    while running:
        server.listen(4)
        (conn, (ip,port)) = server.accept()
        newthread = ClientThread(ip,port) 
        newthread.start() 
        threads.append(newthread) 
    for t in threads:
        t.join()

def startServer():
    Thread(target=startApplicationServer).start()


startServer()
    



