import zlib
import threading
import socket

from reader import PacketReader
from actions import login, send_chat
from util import varint2int, format00
from conf import *

pending = []
run = True

def read_gen(s:socket.socket, read: PacketReader):
    global pending
    while run:
        d = read.get()
        if d == b"": break
        if d[:2] == b"\x00\x0c":
            s.send(b"\x06\x00\x07?\x00\x00\x00")
        if d[:2] == b"\x00$": # $ => \x24
            s.send(format00(21, d[2:]))
            
        n, l = varint2int(d)
        if n >= 256:
            d = zlib.decompress(d[l:])
            if d[0] == 55:
                d = d[17:]
                n, l = varint2int(d)
                d = d[l+1:]
                n, l = varint2int(d)
                message = d[l:n+l]
                a = d.split((b"/tell "))
                n, l = varint2int(a[0][-1:])
                sender = a[1][:n-7]
                pending.append((sender, message))
        
def getter():
    global pending
    while run:
        if not len(pending) == 0:
            d = pending.pop(-1)
            print(f"{d[0].decode('utf-8')}: {d[1].decode('utf-8')}")

def sender(s:socket.socket, username:str):
    while True:
        data = input()
        send_chat(data, s)
        
        

def main():
    username = input("username: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    read = PacketReader(s)
    login(s, read, username=username)
    thread_p = threading.Thread(target=read_gen, args=(s, read))
    thread_g = threading.Thread(target=getter)
    thread_s = threading.Thread(target=sender, args=(s, username))
    thread_p.start()
    thread_g.start()
    thread_s.start()
    
    
if __name__ == "__main__":
    main()