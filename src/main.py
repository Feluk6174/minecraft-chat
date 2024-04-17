import socket
import threading
import sys

from reader import PacketReader
from conf import *
from actions import login, read_gen, send_chat

def main(username="Test"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        thread = threading.Thread(target=send_chat, args=("Monolith!"+username, s, 0,))
        read = PacketReader(s)
        login(s, read, username=username)
        thread.start()
        read_gen(s, read)
        
        
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        main()
    else:
        main(sys.argv[1])
        