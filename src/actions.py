import socket
import time
import random
import zlib

from util import format, format00, varint, to_string, log, varint2int
from reader import PacketReader
from conf import *

def login(s:socket.socket, read:PacketReader, username:str="Test"):
    # Handshacke
    log("Client sending handshake", postfix=format(0, varint(765) + to_string(HOST) + b"\x57\x91" + b"\x02"))
    s.send(format(0, varint(765) + to_string(HOST) + b"\x57\x91" + b"\x02"))
    
    # Login start
    log("Client sending login start", postfix=to_string(username)+b"\x00\x01\x02\x03\x00\x01\x02\x03\x00\x01\x02\x03\x00\x01\x02\x03")
    s.send(format(0, to_string(username)+b"\x00\x01\x02\x03\x00\x00\x02\x03\x00\x01\x02\x03\x00\x01\x02\x03"))
    
    log(read.get(), prefix="Server:")
    log(read.get(), prefix="Server:")
    
    # Login succes
    s.send(format(0, b"\x03"))
    
    # Configuration I think
    log("Client sending configuration")
    s.send(b"\x1a\x00\x01\x0fminecraft:brand\x07vanilla")
    s.send(b"\x0f\x00\x00\x05en_us\x08\x00\x01\x7f\x01\x01\x01")
    
    # Configuration aknowledgement
    while True:
        d = read.get()
        if d == b"": break
        log(d, prefix="Server:")
        if d[-3:] == b"\x00\x02":
            s.send(b"\x02\x00\x02")
            break
        
    log("Login success")
    
def read_gen(s:socket.socket, read: PacketReader):
    while True:
        d = read.get()
        if d == b"": break
        if d[:2] == b"\x00\x0c":
            log("chunks", d)
            s.send(b"\x06\x00\x07?\x00\x00\x00")
        if d[:2] == b"\x00$": # $ => \x24
            log("klkmnm", d)
            s.send(format00(21, d[2:]))
            
        n, l = varint2int(d)
        if n >= 256:
            print("Long boiiii:", zlib.decompress(d[l:]))
            
        log(d, "Server: ", d[:2])
        
def send_chat(message:str, s:socket.socket(), n:int=0):
    time.sleep(5)
    content = to_string(message)+int(time.time()).to_bytes(8, "big")+random.randbytes(8)+b"\x00"+varint(n)+b"\x00\x00\x00"
    s.send(format00(5, content))
    
