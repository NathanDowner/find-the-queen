import sys
from enums import *
from constants import ENCODING_SCHEME, HOST, PORT
from utils import *
from _thread import *
import random
import socket

ROUNDS = 5
currentRound = 1
dealerScore = 0
spotterScore = 0


# def threaded_client(conn: socket.socket):
#     # conn.sendall(messageToBytes(
#     #     f'Welcome to the game', ServerMessageType.HELLO)
#     # )

#     while True:
#         try:
#             data = receiveMessage(conn)  # conn.recv(2048)
#             if not data:
#                 break
#             print(f'received: {data}')
#             conn.sendall(messageToBytes(data, ServerMessageType.HELLO))
#         except:
#             break
#     print('Lost connection')
#     conn.close()


def processMsgs(spotter: socket.socket, socketMsg: str):
    global currentRound
    global dealerScore
    global spotterScore

    status, msg = getParts(socketMsg)
    while True:

        if status == ClientMessageType.S_GUESS.value:
            selection = input(
                'Select a position for the queen. Select either 1,2 or 3\nPosition: ').strip()

            if selection != msg:
                dealerScore += 1
            else:
                spotterScore += 1
            currentRound += 1
            if currentRound < ROUNDS + 1:
                spotter.sendall(messageToBytes(
                    ServerMessageType.REQUEST_S_GUESS,
                    f"\nRound {currentRound}\nScores: Dealer {dealerScore}, Spotter {spotterScore}")
                )
                return 1
            break

        else:
            return 0
    print('Game over!')
    dealerPos, spotterPos = getFinisingPosition(dealerScore, spotterScore)
    spotter.sendall(messageToBytes(ServerMessageType.INFO, spotterPos))
    print(dealerPos)
    spotter.sendall(messageToBytes(
        ServerMessageType.GAME_OVER, 'Thanks For Playing'))
    print('Thanks For Playing')
    return 0


def main():
    """Driver function for the project"""

    print('Find The Queen server')
    print('Welcome Dealer')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        s.listen(1)
        print('Listening for spotter connection')
        while True:
            spotterConn, addr = s.accept()
            print(f'connected to {addr}. \n')
            spotterConn.sendall(messageToBytes(
                ServerMessageType.REQUEST_S_GUESS))
            with spotterConn:
                status = 1
                while (status == 1):
                    msg = receiveMessage(spotterConn)
                    if not msg:
                        status = -1
                    else:
                        status = processMsgs(spotterConn, msg)
                if status < 0:
                    print("Invalid data received. Closing")
                spotterConn.close()
                print("Closed connection socket")
                sys.exit()

            # start_new_thread(threaded_client, (dealer,))


if __name__ == "__main__":
    main()
