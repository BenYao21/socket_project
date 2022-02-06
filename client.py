#!/usr/bin/python
#client.py
from select import select
import socket
from enum import Enum

DISCONNECT_MESSAGE = "!DISCONNECT"

class Requests(Enum): #Requests players may make
    register = 1
    query_players = 2
    start_game = 3
    query_games = 4
    end = 5
    de_register = 6

class Player:

    BUFFER = 1024
    PORT = 6000
    FORMAT = 'utf-8'
    SERVER = "192.168.0.123"
    ADDR = (SERVER, PORT)

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.connect(self.ADDR)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        self.client.sendto(message, self.ADDR)
        print(self.client.recvfrom(self.BUFFER).decode(self.FORMAT))
    def start_game(self, name):
        self.client.sendto(Requests.start_game, self.ADDR)
        self.client.sendto(name, self.ADDR)
    def shuffle():
        pass
    def deal():
        pass
    def play():
        pass

newPlayer = Player()
newPlayer.send("Hello, world!")
input()

newPlayer.send(DISCONNECT_MESSAGE)