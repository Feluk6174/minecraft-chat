import socket
import threading

from reader import PacketReader

def relay(src:PacketReader, des:socket.socket, id:str="Test:"):
    while True:
        data = src.get_raw()
        print(id+": ", data)
        des.send(data)
        if data == b"": break
        
HOST = "matcad_peix.aternos.me"
PORT = 22417

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.bind(("127.0.0.1", 6666))
s1.listen()

# s1 proxy
# conn conneccio minecraft proxy
# s2 conneccio servidor, proxy

# conn client <-> proxy
# s2 proxy <-> server
while True:
    try:
        conn, addr = s1.accept()
        conn_read = PacketReader(conn)
        print("connected by", addr)
        s2.connect((HOST, PORT))
        s2_read = PacketReader(s2)
        print("connected to", HOST, PORT)


        thread_c = threading.Thread(target=relay, args=(conn_read, s2, "Client",))
        thread_c.start()
        
        thread_s = threading.Thread(target=relay, args=(s2_read, conn, "Server",))
        thread_s.start()
        
    except KeyboardInterrupt as e:
        conn.close()
        s1.close()
        s2.close()
        break