#import socket modules
import socket
import sys
import threading

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
PASSWORD = sys.argv[2]
LIMIT = 20
ACTIVE = [] #currently connected users

#function sends message to all clients connected to server
def broadcast(message):
    for user in ACTIVE:
        user[1].sendall(message.encode()) 
    print(message.strip())

#function to keep listening to messages from client
def listener(client, username):
    while True:
        #recieve message from client
        response = client.recv(1024).decode('utf-8')
        
        #check if response is empty
        if response == ':Exit\n' or response == '':
            response = username + " left the chatroom\n"
            for users in ACTIVE:
                if users[0] == username:
                    ACTIVE.remove((username, client))
            broadcast(response)
            client.close()
            break
        elif (response.split(" ")[0] == ':dm'):
            try:
                direct = response.split(" ", 2)

                message = username + " -> " + direct[1] + ": " + direct[2] + "\n"
                
                for user in ACTIVE:
                    if (user[0] == username or user[0] == direct[1]):
                        user[1].sendall(message.encode()) 
                print(message.strip())
            except:
                #send message to all clients if not working 
                message = username + ": " + response
                broadcast(message)
        elif response != '':
            #send message to all clients
            message = username + ": " + response
            broadcast(message)
        else:
            print("Empty message")
            
#function to handle client
def handler(client):
    #listen for client message with username
    while True:
        data = client.recv(1024).decode('utf-8').split("\n")
        password = data[0]
        username = data[1]
        if (password.strip() == PASSWORD.strip()):
            #check if user already exist
            exists = False
            for users in ACTIVE:
                if (users[0] == username):
                    exists = True
            if (exists):
                client.close()
                break
            else:
                #send joined chatroom message to all clients
                joined = username + " joined the chatroom\n"
                broadcast(joined)
                #add client
                ACTIVE.append((username, client))
                
                #send welcome message to new client
                message = "Welcome!\n"
                client.sendall(message.encode())
                #thread to listen to new client
                threading.Thread(target=listener, args=(client,username, )).start()
                break
        else:
            message = "Incorrect Password!\n"
            client.sendall(message.encode())
            client.close()
    
#main function
def main():
    #creating the server socket object for communication 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(IPv4, TCP packets)
    
    try:
        server.bind((HOST, PORT)) 
        print(f"Server started on port {PORT}. Accepting connections...")
    except:
        print("Didn't work")
    
    #set server limit - how many connections
    server.listen(LIMIT)
    
    #keep listening for client
    while True:
        client, address = server.accept()
        threading.Thread(target=handler, args=(client, )).start()
    

if __name__ == '__main__':
    main()
    
    