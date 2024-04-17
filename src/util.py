def varint(value:int) -> bytes:
    s = []
    for i in range(3):
        s.append(f"{(value & 127):07b}")
        value >>= 7
        if value == 0:
            break
        
    res = ""
    for i, val in enumerate(s):
        res += ("1" if not len(s)-1 == i else "0") + val
        
    return bin2bytes(res)

def bin2bytes(val:str) -> bytes:
    h = hex(int(val, 2))[2:]
    if len(h) % 2 == 1:
        h = "0"+h
    return bytes.fromhex(h)

def int2bytes(val:int) -> bytes:
    h = hex(val)[2:]
    if len(h) % 2 == 1:
        h = "0"+h
    return bytes.fromhex(h)

def format(id:int, content:bytes):
    body = varint(id)+content
    return varint(len(body)) + body

def format00(id:int, content:bytes):
    body = b"\x00"+varint(id)+content
    return varint(len(body)) + body

def varint2int(val:bytes) -> int:
    val = val.hex()
    n = len(val)//2
    res = 0
    for i in range(n):
        num = int(val[i*2:i*2+2], 16)
        next = bool((num & 128))
        num &= 127
        res |= (num << (7*i))
        if not next:
            return res, i+1
    return res, 0

def to_string(s:str) -> bytes:
    b = s.encode("utf-8")
    b = varint(len(b)) + b
    return b

def log(data:str, prefix:str="", postfix:str=""):
    print(prefix, data, postfix)