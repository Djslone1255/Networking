import socket

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 7765
BOARDSIZE = 3
LENGTH = 3
MAXPLAYERS = 2

class Square():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
    def findWin(self, board, depth):
        if(self.value == '0'):
            return False
        win = False
        i = 1
        while i < LENGTH:
            if(self.x+i >= board.boardSize):
                break
            elif(board.getSquare(self.x+i, self.y).value != self.value):
                break
            if(i + 1 == LENGTH):
                win = True
            i += 1
        i = 1
        while i < LENGTH:
            if(self.y+i >= board.boardSize):
                break
            elif(board.getSquare(self.x, self.y+i).value != self.value):
                break
            if(i + 1 == LENGTH):
                win = True
            i += 1
        i = 1
        while i < LENGTH:
            if((self.x+i >= board.boardSize) or (self.y+i >= board.boardSize)):
                break
            elif(board.getSquare(self.x+i, self.y+i).value != self.value):
                break
            if(i + 1 == LENGTH):
                win = True
            i += 1
        i = 1
        while i < LENGTH:
            if((self.x == 0) or (self.y+i >= board.boardSize)):
                break
            elif(board.getSquare(self.x-i, self.y+i).value != self.value):
                break
            if(i + 1 == LENGTH):
                win = True
            i += 1
        return win


class Board():
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.board = []
        for i in range(boardSize*boardSize):
            sq = Square((i % boardSize), int(i / boardSize), '0')
            self.board.append(sq)
    def getSquare(self, x, y):
        return self.board[x + int(y*self.boardSize)]
    def clearboard(self):
        for x in self.board:
            x.value = '0'
    def displayBoard(self):
        display = " "
        number = 0
        for col in range(self.boardSize):
            display += f'{number}'
            number += 1
        number = 0
        display += "\n"
        for line in range(self.boardSize):
            display += f'{number}'
            for col in range(self.boardSize):
                display += self.getSquare(col, line).value
            display += "\n"
            number += 1
        return display


def recive_cmd(client_socket):
    try:
        msg_header = client_socket.recv(HEADERSIZE)
        
        msg_leng = int(msg_header.decode("utf-8").strip())
        msg = client_socket.recv(msg_leng).decode("utf-8")
        return msg
    except:
        return False

def gameMove(cmd, board, player):
    try:
        x = int(cmd[0])
        y = int(cmd[2])
    except:
        return 0
    msg = ''
    if(x >= board.boardSize or y >= board.boardSize):
        #msg = "invalid space"
        return 0
    elif b.getSquare(x, y).value != '0':
        #msg = "invalid space"
        return 0
    else:
        b.getSquare(x, y).value = player
        msg = board.displayBoard()
    for element in board.board:
        if element.findWin(b, player):
            return 2
    return 1

        
def sendMessage(msg):
    msg = f'{len(msg):<{HEADERSIZE}}'+ msg

    clientsocket.send(bytes(msg, "utf-8"))  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(5)

print("server runnin")

while True:
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established!")
    b = Board(BOARDSIZE)

    msg = "Welcom to the server!\n" 
    msg += b.displayBoard()
    msg += "it is X's turn"

    sendMessage(msg)  

    msg = b.displayBoard()
    msg += "it is your turn"  
    print(msg)

    game = True

    while game:

        turn = True
        while turn:
            cmd = input(": ")
            if cmd:
                over = gameMove(cmd, b, "X")
                if over == 2:

                    msg = b.displayBoard()
                    msg += "player X wins\n"
                    b.clearboard()
                    msg += b.displayBoard()
                    cmsg = msg
                    msg += "\n it is your turn"

                    sendMessage(msg)
                    cmsg += "\n it is O's turn"  
                    print(cmsg)
                    turn = False
                elif over == 0:
                    print("invalid input\ntry again")
                elif over == 1:
                    msg = b.displayBoard()
                    msg += "\n it is your turn"

                    sendMessage(msg)
                    msg = b.displayBoard()
                    msg += "\n it is O's turn"  
                    print(msg)
                    turn = False
                else:
                    print("critical error")
        
        
        
        turn = True
        while turn:
            cmd = recive_cmd(clientsocket)
            if not cmd:
                print("client disconected")
                game = False
                break
            over = gameMove(cmd, b, "O")
            if over == 2:
                msg = b.displayBoard()
                msg += "player O wins\n"
                b.clearboard()
                msg += b.displayBoard()
                cmsg = msg
                msg += "\n it is X's turn"

                sendMessage(msg)
                cmsg += "\n it is your turn"  
                print(cmsg)
            elif over == 0:
                msg = "invalid input"
                sendMessage(msg)
                msg = "try again"
                sendMessage(msg)
            elif over == 1:
                msg = b.displayBoard()
                msg += "\n it is X's turn"

                sendMessage(msg)
                msg = b.displayBoard()
                msg += "\n it is your turn"  
                turn = False
            else:
                print("critical error")   

        
        print(msg)
                

