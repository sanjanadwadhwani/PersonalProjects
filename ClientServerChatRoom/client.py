#import socket modules
from datetime import datetime
import socket
import threading
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
PASSWORD = sys.argv[3]
USERNAME = sys.argv[4]

#listen for messages from server
def listener(client):
    while True:
        #receive message from server
        message = client.recv(1024).decode('utf-8')
        message = message.strip()
        #check if message is empty and print if not
        if message != '':
            print(message)
        else:
            break
                 
def sendMessages(client):
    while True:
        #recieve input
        message = input().strip()
        #command inputs 
        if (message == ':)'):
            message = "[feeling happy]"
        if (message == ':('):
            message = "[feeling sad]"
        if (message == ':mytime'):
            today = datetime.now()
            message = today.strftime("It's %H:%M on %a, %d %b, %Y.")
        message += "\n"
        client.sendall(message.encode())
            
        if (message == ':Exit\n'):
            client.shutdown(socket.SHUT_RDWR)
            sys.exit(0)
            
#main function
def main():
    #creating the server socket object for communication 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to {HOST} on port {PORT}...")
    #connect to server
    client.connect((HOST, PORT))
    
    try:
        client.send((f'{PASSWORD}\n').encode())
        client.send((f'{USERNAME}\n').encode())
        
        message = client.recv(1024).decode()
    except:
        print("Error")
        sys.exit(1)
        
    if (message == 'Welcome!\n'):
        print(message.strip())
        threading.Thread(target=listener, args=(client, )).start()
        sendMessages(client)
    else:
        print(message)

if __name__ == '__main__':
    main()