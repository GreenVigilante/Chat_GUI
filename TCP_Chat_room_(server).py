import threading
import socket

host = "localhost"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nickname = []

def blast(message):
    for client in clients:  
        print(message)
        client.send(message)

def handle(client):
    while True:
        try:
            mess = message = client.recv(1024)
            if mess.decode("ascii").startswith("kick"):
                if nickname[clients.index(client)] == "admin":
                    name_kick = mess.decode("ascii")[5:]
                    kick(name_kick)
                else:
                    client.send("You aint no admin!\n".encode("ascii"))
            elif mess.decode("ascii").startswith("ban"):
                if nickname[clients.index(client)] == "admin":
                    name_ban = mess.decode("ascii")[4:]
                    ban(name_ban)
                    with open("ban.txt", "a") as f:
                        f.write(f"{name_ban}\n")
                    print(f"{name_ban} has been banned")
                else:
                    client.send("You aint no admin!\n".encode("ascii"))
            else:
                blast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname1 = nickname[index]
                blast(f"{nickname1} has left the chat. How sad :(\n".encode("ascii"))
                print(f"{nickname1} has left!")
                nickname.remove(nickname1)
            break
def kick(name):
    if name in nickname:
        index_name = nickname.index(name)
        clients_kick = clients[index_name]
        clients_kick.send("You have been kicked!\n".encode("ascii"))
        nickname.remove(name)
        clients.remove(clients_kick)
        clients_kick.close()
        blast(f"{name} has been kicked!\n".encode("ascii"))
def ban(name):
    if name in nickname:
        index_name = nickname.index(name)
        clients_kick = clients[index_name]
        clients_kick.send("You have been ban!\n".encode("ascii"))
        nickname.remove(name)
        clients.remove(clients_kick)
        clients_kick.close()
        blast(f"{name} has been ban!\n".encode("ascii"))

def receive():
    while True:
    
        client, addr = server.accept()
        print(f"Connected to {str(addr)}")
        client.send("Nickname: ".encode("ascii"))
        clients.append(client)
        nickname1 = client.recv(1024).decode("ascii")
        if nickname1 in nickname:
            client.send("CHOOSEN".encode("ascii"))
            clients.remove(client)
            client.close()
            continue
        with open("ban.txt", "r") as f:
            bans = f.readlines()
        
        if nickname1+"\n" in bans:
            client.send("BAN".encode("ascii"))
            clients.remove(client)
            client.close()
            continue
        if nickname1 == "admin":
            client.send("adminjumpsin".encode("ascii"))
            password_admin = client.recv(1024).decode("ascii")
            if password_admin != "holaiamadmin":
                client.send("NO".encode("ascii"))
                client.close()
                print("Some one tried to be sneaky")
                clients.remove(client)
                continue
        nickname.append(nickname1)
        print(f"Client {nickname1} has joined")
        blast(f"{nickname1} has joined the chat :)\n".encode("ascii"))
        client.send("Connected to server!\n".encode("ascii"))

        t = threading.Thread(target=handle, args=(client, ))
        t.start()
print("Server is running ...")
receive()