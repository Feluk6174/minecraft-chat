import socket
import threading

from util import varint, varint2int

class PacketReader:
    def __init__(self, s:socket.socket):
        self.s = s
        self.in_queue = []
        self.temp = b""
        self.run = True
        
        thread = threading.Thread(target=self.reciever)
        thread.start()
        
    def reciever(self):
        while self.run:
            self.in_queue.append(self.s.recv(1024))
            
    def read(self):
        while True:
            try:
                return self.in_queue[0]
            except IndexError:
                pass
            
    def get_raw(self):
        getting = True
        temp = b""
        n = 0
        d = self.read()
        l, i = varint2int(d) 
        n += l + i
        while getting:
            if len(d) > l + i - len(temp):
                self.in_queue[0] = d[l+i -len(temp):]
                temp += d[:n-len(temp)]
            else:
                temp += d
                self.in_queue.pop(0)
            if len(temp) == n:
                getting = False
                return temp
                
            d = self.read()
        
    def get(self):
        d = self.read()
        l, i = varint2int(d)
        return self.get_raw()[i:]
    
    def put(self, arg):
        self.in_queue.append(arg)          
            
    def stop(self):
        self.run = False
        self.s.close()
        
        
if __name__ == "__main__":
    pr = PacketReader(socket.socket())
    pr.put(b"\x07\x00\x01\x02\x03\x04")
    pr.put(b"\x05\x06\x02\x00\x01")
    print(pr.get())
    print(pr.get())