#!/usr/bin/python

'''
manager.py
author: chao yao
lastest edit: 02/05 2022
'''
from http import server
from ipaddress import ip_address
import socket
import threading
import random
from sys import exit, flags
from enum import Enum
from urllib import request
users = set()#an easy "database" to store user information
games = set()#an easy "database" to store game information
class Requests(Enum): #Requests players may make
    register = 1
    query_players = 2
    start_game = 3
    query_games = 4
    end = 5
    de_register = 6

class Game: #construct a game object
    players = set()
    def __init__(self, id):
        self.id = id
    def assign_dealer(self, user):
        user.tag = "dealer"
        user.in_game = True
    def assign_player(self):
        for player in users:
            if player.id is not self.id and player.in_game:
                self.players.add(player)
                player.in_game = True
class User: #construct a user object
    id = 0
    tag = "player"
    in_game = False
    def __init__(self, name, ip, port_num):
        self.name = name
        self.ip = ip
        self.port = port_num

class Manager: 
    BUFFER = 1024
    PORT = 6000 #range: (6000, 6499)
    SERVER = socket.gethostbyname(socket.gethostname()) #get host 
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)#bind server
    DISCONNECT_MESSAGE = "!DISCONNECT"

    def __init__(self):
        '''
        self.server.listen()
        '''
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            data, addr = self.server.recvfrom(self.BUFFER)
            thread = threading.Thread(target = self.handle_client, args= (addr[0], addr[1]))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    def handle_client(self, conn, addr):
        connected = True
        while connected: 
            msg, addr = self.server.recvfrom(self.BUFFER).decode(self.FORMAT)
            if msg == self.DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            if msg == Requests.start_game:
                pass
            elif msg == Requests.query_players:
                pass
            elif msg == Requests.start_game:
                pass
            elif msg == Requests.query_games:
                pass
            elif msg == Requests.end:
                pass
            elif msg == Requests.de_register:
                pass
            else:
                self.server.sendto("Wrong requests".encode(), self.addr)

    def register(self,user, ip_addr, port):
        newUser = User(user, ip_addr, port)
        if(newUser in users):
            self.server.sendto("FAILURE".encode(), self.addr)
        else:
            users.add(newUser)
            self.server.sendto("SUCCESS".encode(), self.addr)
    def query_players(self):
        self.server.sendto(len(users).to_bytes, self.addr)
        for user in users:
            self.server.sendto(user.encode(), self.addr)
    def start_game(self, user, k):
        if(not(user in users or k < 1 or k > 3 or k < len(users))):
            self.server.sendto("FAILURE".encode(), self.addr)
        else:
            self.server.sendto("SUCCESS".encode(), self.addr)
            newGame = Game(user)
            newGame.assign_dealer(user)
            newGame.assign_player()
            for p in users:
                self.server.sendto(f"player {p.name} registered in game with ID {newGame.id}".encode(), self.addr)   
    def query_games(self):
        for game in games:
            self.server.sendto(f"game with ID {game.id} is running".encode(), self.addr)
    def end(self, game_id):
        for game in games:
            if game.id == game_id:
                games.remove(game)
    def de_register(self, user):
        users.remove(user)

print("[STARTING] server is starting...")
manager = Manager()