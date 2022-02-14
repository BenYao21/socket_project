#!/usr/bin/python
"""
client.py
author: chao yao
latest edit: 02/13 2022
"""
from select import select
import socket

class Player:

    BUFFER = 1024
    REMOTE_PORT = 6000
    SOURCE_PORT1 = 6001
    SOURCE_PORT2 = 6002
    FORMAT = 'utf-8'
    REMOTE_SERVER = "192.168.0.123"
    LOCAL_SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (REMOTE_SERVER, REMOTE_PORT)

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((self.LOCAL_SERVER, self.SOURCE_PORT1))
        self.deal_with_actions()

    '''
    author: chao yao
    lastest edit: 02/13 2022
    @Parameters: 
    @Returns:
    This method identify different player requests and call different methods
    to deal with it.
    '''
    def deal_with_actions(self):
        while True:
            req_input = input("Enter your request: ")
            method = getattr(self, req_input)
            method()
    def register(self):
        userName = input("Enter your user name:")
        ip_addr = self.LOCAL_SERVER
        port = self.SOURCE_PORT1
        args = ("register",userName, str(ip_addr), str(port))
        msg = "\n".join(args)
        self.client.sendto(msg.encode(self.FORMAT), self.ADDR)
        print(self.client.recvfrom(self.BUFFER)[0].decode(self.FORMAT))
    def query_players(self):
        msg = "query_players"
        self.client.sendto(msg.encode(self.FORMAT), self.ADDR)
        print(self.client.recvfrom(self.BUFFER)[0].decode(self.FORMAT))
    def start_game(self):
        msg = "start_game"
        k = input("Enter number of players you want to play with you(1~3): ")
        args = (msg, k)
        data = "\n".join(args)
        self.client.sendto(data.encode(self.FORMAT), self.ADDR)
    def query_games(self):
        msg = "query_games"
        self.client.sendto(msg.encode(self.FORMAT), self.ADDR)
        print(self.client.recvfrom(self.BUFFER)[0].decode(self.FORMAT))
    def end(self):
        msg = "end"
        self.client.sendto(msg.encode(self.FORMAT), self.ADDR)
    def de_register(self):
        msg = "de_register"
        self.client.sendto(msg.encode(self.FORMAT), self.ADDR)
        print(self.client.recvfrom(self.BUFFER)[0].decode(self.FORMAT))
    def shuffle():
        pass
    def deal():
        pass
    def play():
        pass

newPlayer = Player()