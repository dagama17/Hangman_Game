import os
import sys
import time
import json
import socket
import threading

IP_ADDR = "<your_ip_address>"
PORT = 4444
all_clients = []
current_dir = os.getcwd()
lines = "\t" + "_" * 60

logo = r"""

                 _   _    _    _   _  ____ __  __    _    _   _ 
                | | | |  / \  | \ | |/ ___|  \/  |  / \  | \ | |
                | |_| | / _ \ |  \| | |  _| |\/| | / _ \ |  \| |
                |  _  |/ ___ \| |\  | |_| | |  | |/ ___ \| |\  |
                |_| |_/_/   \_\_| \_|\____|_|  |_/_/   \_\_| \_|
                                                                    
                     ____  _____ ______     _______ ____  
                    / ___|| ____|  _ \ \   / / ____|  _ \ 
                    \___ \|  _| | |_) \ \ / /|  _| | |_) |
                     ___) | |___|  _ < \ V / | |___|  _ < 
                    |____/|_____|_| \_\ \_/  |_____|_| \_\

"""

def clients(conn):
    # get all clients username from the database
    users = {}
    all_users = [] 
    with open(f"C:\\Users\\israe\\Documents\\Evil_Tech\\hangman_cli\\database.json", "r") as file:
        contents = json.load(file)
        
        # for cl in contents["database"]:
        #     users.update(cl)

    for i in contents['database']:
        for x in i.values():
            all_users.append(x)

    
    conn.send("client_name".encode("utf-8"))
    client = conn.recv(1024).decode("utf-8")

    
    #message = conn.send("joined the game".encode("utf-8"))
    

    if client in all_users:
        # first we will check if the client is in the database before we send to other users that he joined
        # here we are going to broadcast the message to all clients
        connected = True
        all_clients.append(client)
            
        active = len(all_clients) 
        unactive = len(contents["database"]) - len(all_clients)
        
        while connected:
            os.system("cls" if os.name == "nt" else "clear")
            print(logo)
            print(lines)
            #while connected:
            
            print(f"\n\t[+] all active number of clients: {active}")
            print(f"\t[-] all unactive number of clients: {unactive}\n")
            #what if the user leaves the game we need to some how check for updates in the all_clients list
           
            cmd = input("\t>>> ")

            if cmd == "active users":
                users0 = ", ".join(x for x in all_clients)
                print(f"\t{users0}")
                time.sleep(4)
            
            if cmd == "unactive users":
                info = []
                users = {}
                for i in contents['database']:
                    for x in i.values():
                        info.append(x)

                for j in all_clients:
                    if j in info:
                        info.remove(j)
                        users.update(j)

                print(f"\t{users}")
                time.sleep(4)

           
    else:
        # If the user doen't exist then we will close the program
        
        print(f"\t[!] invalid user name: {client}")
        conn.send("exit".encode("utf-8"))


    data = conn.recv(1024).decode("utf-8")
    if type(data) == dict:
        print(data)
    # Then we will compare if the users is in the database then he can play

def start_server():
    
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((IP_ADDR, PORT))
    serv.listen()

    connected = True

    while connected:

        conn, ip_addr = serv.accept()
        conn.setblocking(1) # no timeout

        thread = threading.Thread(target=clients, args=(conn,))
        thread.start()

    serv.close()

    
if __name__ == "__main__":

    try:
        os.system("cls" if os.name == "nt" else "clear")
        print(logo)
        print(lines)
        print(f"\n\t[-] Waiting for users to join the game on port:{PORT}")
        start_server()

    except KeyboardInterrupt as e:
        print(e)
