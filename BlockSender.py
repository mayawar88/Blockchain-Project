import socket
import random 
from math import ceil 
from decimal import *
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import json

global field_size 
field_size = 10**5
global normal_storage
global block_storage

main = Tk()
main.title("Blockchain for Secure EHRs Sharing of Mobile Cloud Based E-Health Systems")
main.geometry("1300x1200")

def reconstructSecret(shares):       
    # Combines shares using  
    # Lagranges interpolation.  
    # Shares is an array of shares 
    # being combined 
    sums, prod_arr = 0, []       
    for j in range(len(shares)): 
        xj, yj = shares[j][0],shares[j][1] 
        prod = Decimal(1) 
          
        for i in range(len(shares)): 
            xi = shares[i][0] 
            if i != j: prod *= Decimal(Decimal(xi)/(xi-xj)) 
                  
        prod *= yj 
        sums += Decimal(prod) 
          
    return int(round(Decimal(sums),0)) 
   
def polynom(x,coeff):       
    # Evaluates a polynomial in x  
    # with coeff being the coefficient 
    # list 
    return sum([x**(len(coeff)-i-1) * coeff[i] for i in range(len(coeff))]) 
   
def coeff(t,secret):       
    # Randomly generate a coefficient  
    # array for a polynomial with 
    # degree t-1 whose constant = secret''' 
    coeff = [random.randrange(0, field_size) for _ in range(t-1)] 
    coeff.append(secret)       
    return coeff 
   
def generateShares(n,m,secret):       
    # Split secret using SSS into 
    # n shares with threshold m 
    cfs = coeff(m,secret) 
    shares = []       
    for i in range(1,n+1): 
        r = random.randrange(1, field_size) 
        shares.append([r, polynom(r,cfs)])       
    return shares 

def shareBlock():
    global normal_storage
    global block_storage
    text.delete('1.0', END)
    data = int(tf1.get().strip())
    t,n = 5, 7    
    secret = data
    text.insert(END,'Block Data : ', str(secret)+"\n") 
    # Phase I: Generation of shares 
    shares = generateShares(n, t, secret)
    normal_storage = len(str(shares).encode('utf-8')) / 1000
    length = len(shares)
    share1 = ''
    share2 = ''
    num_block = length / 2
    j = 0
    for i in range(len(shares)):
        if j < num_block:
            value = str(shares[i])
            value = value[1:len(value)-1]
            value = value.split(",")
            value[0] = value[0].strip()
            value[1] = value[1].strip()
            share1+=value[0]+","+value[1]+" "
            j = j + 1
        elif j >= num_block:
            value = str(shares[i])
            value = value[1:len(value)-1]
            value = value.split(",")
            value[0] = value[0].strip()
            value[1] = value[1].strip()
            share2+=value[0]+","+value[1]+" "
            j = j + 1
    text.insert(END,'Data sharing with block chain node 1 : '+share1+"\n")
    text.insert(END,'\nData sharing with block chain node 2 : '+share2+"\n\n")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(('localhost', 2222))
    jsondata = json.dumps({"type": 'store', "data": share1})
    message = client.send(jsondata.encode())
    data = client.recv(100)
    data = data.decode()
    text.insert(END,data+"\n")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(('localhost', 3333))
    jsondata = json.dumps({"type": 'store', "data": share2})
    message = client.send(jsondata.encode())
    data = client.recv(100)
    data = data.decode()
    text.insert(END,data+"\n")
    block_storage = len(str(share1).encode('utf-8')) / 1000

def reconstructBlock():
    text.delete('1.0', END)
    index = int(tf1.get().strip())
    t,n = 5, 7
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(('localhost', 2222))
    jsondata = json.dumps({"type": 'get', "data": str(index)})
    message = client.send(jsondata.encode())
    data = client.recv(10000)
    share1 = data.decode().strip()
    text.insert(END,'Received share1 : '+share1+"\n")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(('localhost', 3333))
    jsondata = json.dumps({"type": 'get', "data": str(index)})
    message = client.send(jsondata.encode())
    data = client.recv(10000)
    share2 = data.decode().strip()
    text.insert(END,'Received share2 : '+share2+"\n")

    combine_share = []
    first = share1.strip().split(" ")
    second = share2.strip().split(" ")
    for i in range(len(first)):
        arr = first[i].split(",")
        f = int(arr[0])
        s = int(arr[1])
        temp = [f,s]
        combine_share.append(temp)
    for i in range(len(second)):
        arr = second[i].split(",")
        f = int(arr[0])
        s = int(arr[1])
        temp = [f,s]
        combine_share.append(temp)    
    print(combine_share)
    pool = random.sample(combine_share, t) 
    text.insert(END,"\nReconstructed original value :"+str(reconstructSecret(pool)))

    
    
def graph():
    height = [normal_storage,block_storage]
    bars = ('Normal Blockchain Storage', 'Propose Secret Share Storage')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
    
font = ('times', 15, 'bold')
title = Label(main, text='Light Repository Blockchain System with Multisecret Sharing for Industrial Big Data')
title.config(bg='mint cream', fg='olive drab')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
ff = ('times', 12, 'bold')

l1 = Label(main, text='Enter Block Data:')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=40)
tf1.config(font=font1)
tf1.place(x=230,y=100)

runButton = Button(main, text="Share Blocks", command=shareBlock)
runButton.place(x=50,y=150)
runButton.config(font=ff)

uploadButton = Button(main, text="Retrieve & Reconstruct Block", command=reconstructBlock)
uploadButton.place(x=230,y=150)
uploadButton.config(font=ff)

graphButton = Button(main, text="Storage Graph", command=graph)
graphButton.place(x=480,y=150)
graphButton.config(font=ff)

font1 = ('times', 13, 'bold')
text=Text(main,height=20,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)

main.config(bg='gainsboro')
main.mainloop()







    
