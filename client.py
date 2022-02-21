import socket

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 7765

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))




while True:
    msg_header = s.recv(HEADERSIZE)
        
    msg_leng = int(msg_header.decode("utf-8").strip())
    msg = s.recv(msg_leng).decode("utf-8")
    print(msg)
    
    msg_header = s.recv(HEADERSIZE)
        
    msg_leng = int(msg_header.decode("utf-8").strip())
    msg = s.recv(msg_leng).decode("utf-8")
    print(msg)

    i = True
    while i:
        cmd = input(": ")
        if cmd:
            cmd = cmd.encode("utf-8")
            cmd_header = f"{len(cmd) :< {HEADERSIZE}}".encode("utf-8")
            s.send(cmd_header + cmd)
            i = False
    
    

