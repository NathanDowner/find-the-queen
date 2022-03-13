from enum import Enum
import socket
from constants import HOST, PORT
from enums import ClientMessageType
from utils import messageToBytes, receiveMessage


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = self.connect()
        print(msg)

    def connect(self):
        try:
            self.client.connect((HOST, PORT))
            self.client.sendall(messageToBytes(
                'Hello', ClientMessageType.HELLO))
            return receiveMessage(self.client)
        except:
            pass

    def send(self, message: str, status: Enum):
        try:
            self.client.sendall(messageToBytes(message, status))
        except socket.error as e:
            print(str(e))


n = Network()
print(n.send("hello", ClientMessageType.HELLO))
