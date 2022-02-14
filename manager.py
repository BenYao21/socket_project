#!/usr/bin/python

'''
manager.py
author: chao yao
latest edit: 02/12 2022
'''
import socket
import threading
import random
import time
import uuid

class Game: #construct a game object
    players = set()
    def __init__(self):
        self.id = uuid.uuid4() #uuid4 function will return a id which is 99.99% possiblity not duplicate
    def assign_dealer(self, user):
        user.tag = "dealer"
        user.in_game = True
    def assign_player(self, gamers):
        for gamer in gamers:
            self.players.add(gamer)
            gamer.tag = True

class User: #construct a user object
    id = 0
    tag = "player"
    in_game = False
    def __init__(self, name, ip, port_num):
        self.name = name
        self.ip = ip
        self.port = port_num
        self.in_game = False
    def query_players(self):
        pass
'''
TODO: add multithread support to manager

'''
class Manager: 
    BUFFER = 1024
    PORT = 6000 #range: (6000, 6499)
    SERVER = socket.gethostbyname(socket.gethostname()) #get host 
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)#bind server
    Requests = {}
    users = dict()#an easy "database" to store user information
    games = set()#an easy "database" to store game information

    def __init__(self):
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        self.handle_client()
        #threading.Thread(target = self.handle_client, args= ())
        #print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")
        
    '''
    author: chao yao
    latest edit: 02/13 2022
    @Parameters: 
    @Returns: 
    This method takes messages received from players(clients) and call 
    different methods to handle the client's request.
    ''' 
    def handle_client(self):
        while True:
            time.sleep(0.1)
            data, addr = self.server.recvfrom(self.BUFFER)
            msg = data.decode(self.FORMAT).split("\n")
            method_name = getattr(self, msg[0])
            method_name(data, addr)
            
    def register(self, data, addr):
        ip_addr = addr[0]
        port = addr[1]
        msg = data.decode(self.FORMAT).split("\n")
        user = msg[1]
        newUser = User(user, ip_addr, port)
        if (newUser.ip, newUser.port) in self.users.keys():
            self.server.sendto("FAILURE! Re-register is not supported".encode(), (ip_addr, port))
        else:
            self.users[(ip_addr, port)] = newUser
            self.server.sendto("SUCCESS".encode(), (ip_addr, port))
    def query_players(self, data, addr):
        lengthOfUsers = str(len(self.users.keys())) + " players registered"
        msg = "\n".join((lengthOfUsers, str(self.users)))
        self.server.sendto(msg.encode(self.FORMAT), addr)
    '''
    Multithread support will be added soon. It is not complete now.
    '''
    def start_game(self, data, addr):
        user = data[1]
        k = data[2]
        if(not(user in self.users or k < 1 or k > 3 or k < len(self.users))):
            self.lock.acquire()
            self.server.sendto("FAILURE! Input number of players is not supported!".encode(), addr)
        else:
            self.lock.acquire()
            self.server.sendto("SUCCESS".encode(), addr)
            newGame = Game(random.randrange(1000, 1999))
            newGame.assign_dealer(user)
            random.sample(self.users, k)
            newGame.assign_player()
            for p in self.users:
                self.server.sendto(f"player {p.name} registered in game with ID {newGame.id}".encode(), addr)   
            self.lock.release()
    def query_games(self, data, addr):
        lengthOfGames = str(len(self.games)) + " games are running"
        msg = "\n".join((lengthOfGames, str(self.games)))
        self.server.sendto(msg.encode(self.FORMAT), addr)
    '''
    Multithread support will be added soon. It is not complete now.
    '''
    def end(self, data, addr):
        game_id = data[1]
        for game in self.games:
            if game.id == game_id:
                self.games.remove(game)
    def de_register(self, data, addr):
        user_addr = addr
        user = self.users[user_addr]
        #print(user_addr)
        #print(user.in_game)
        if user.in_game:
            self.server.sendto("FAILURE! The user is in a game!".encode(self.FORMAT), addr)
        else:
            self.server.sendto("SUCCESS!".encode(self.FORMAT), addr)
            self.users.pop(user_addr)
print("[STARTING] server is starting...")
manager = Manager()