from enum import Enum
import socket
from constants import ENCODING_SCHEME


def messageToBytes(status: Enum, msg='') -> bytes:
    """Returns bytes containing the status code and message encoded using the
    global encoding scheme."""
    return f"{status.value} {msg}".encode(ENCODING_SCHEME)


def receiveMessage(socket: socket.socket) -> str:
    """Returns the string form of a message received from the socet and decoded 
    using the global encoding scheme."""

    return socket.recv(2048).decode(ENCODING_SCHEME)


def getParts(socketMessage: str):
    status, *msg = socketMessage.split(' ')
    rest = ' '.join(msg)
    return (status, rest)


def getFinisingPosition(dealerScore, spotterScore):
    if dealerScore > spotterScore:
        return ('VICTORY', 'DEFEAT')
    else:
        return ('DEFEAT', 'VICTORY')
