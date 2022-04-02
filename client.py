from ipaddress import ip_address
import socket, time, threading
import os

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

x, y = input('Enter chat server\'s IP address and port: ').split()
SERVER = x
PORT = int(y)
ADDR = (SERVER, PORT)
nickname = input("Choose a nickname:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receiveClient():
    condition = True
    while condition:
        try:
            msg1 = client.recv(4096)
            if msg1.decode(FORMAT) == "getNickname":
                client.send(nickname.encode(FORMAT))  # if new connection, server will ask user to send nickname

            elif msg1.decode(FORMAT)[:4] == "sent":
                write_name = msg1[5:]
                #if os.path.exists(write_name):os.remove(write_name)
                with open(write_name, 'wb') as file:
                    while 1:
                        data = client.recv(1024)
                        if not data:
                            break
                        file.write(data)
                    file.close()

                print(msg1.decode(FORMAT), 'Successfully downloaded.')

            else:
                print(msg1.decode(FORMAT))  # connection already establish. just print msg


        except:  # any exception = disconnect
            print("Disconnected")
            client.close()
            break
    # f.close()


def write():
    print('Running client program...')
    print(f'Trying to connect to the server: {ADDR}')
    condition = True
    while condition:
        userInput = input("")  # get any msg wants to send across chat
        msg = f'{nickname}:{userInput}'
        client.send(msg.encode(FORMAT))  # send msg to server
        userInput = userInput.lower()  # format string to lower case
        if userInput == DISCONNECT_MESSAGE:  # if user want to disconnect
            client.close()
            break
        elif userInput == "list images":  # send image list to user
            client.send("Image list".encode(FORMAT))
        elif userInput == "download":
            print("Please enter the image name to be downloaded:")
            image_name = input("")
            client.send(image_name.encode(FORMAT))


# run both receive and write threads.
receive_thread = threading.Thread(target=receiveClient)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
