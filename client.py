import socket
import sys
# from network import Network
from enums import *
from constants import ENCODING_SCHEME, HOST, PORT
from utils import receiveMessage, messageToBytes, getParts


def processMsgs(clientSocket: socket.socket,  socketMessage: str):
    status, msg = getParts(socketMessage)
    if msg:
        print(msg)

    if status == ServerMessageType.GAME_OVER.value:
        print('Game over')
        return 0

    if status == ServerMessageType.REQUEST_S_GUESS.value:
        print('Enter a guess of 1, 2 or 3')
        resp = input('Your guess: ').strip()
        clientSocket.sendall(messageToBytes(ClientMessageType.S_GUESS, resp))
        return 1

    if status == ServerMessageType.INFO.value:
        return 1
    else:
        return 0


def main():
    print('Find The Queen client')
    print('You\'re the spotter')
    # n = Network()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        try:
            clientSocket.connect((HOST, PORT))
        except socket.error as e:
            print(str(e))

        while True:
            status = 1
            while(status == 1):
                msg = receiveMessage(clientSocket)
                if not msg:
                    status = -1
                else:
                    status = processMsgs(clientSocket, msg)
            if status < 0:
                # Close the socket.
                clientSocket.close()
                print("Closed connection socket")
                sys.exit()


if __name__ == "__main__":
    main()
