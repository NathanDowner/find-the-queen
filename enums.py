from enum import Enum


class ClientMessageType(Enum):
    HELLO = '1'
    S_GUESS = '3'
    D_SELECTION = '5'
    ACK = '7'
    AUTH_RESPONSE = '9'


class ServerMessageType(Enum):
    HELLO = '2'
    INFO = '4'
    REQUEST_S_GUESS = '6'
    REQUEST_D_SELECTION = '8'
    GAME_OVER = '10'
    REQUEST_AUTH = '12'
