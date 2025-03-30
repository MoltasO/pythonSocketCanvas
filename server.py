from socket import *
import _thread as thread

clientNumber: int = 0

class clientClass:
    def __init__(self, address: tuple[str, int], connection: socket):
        self.connection: socket = connection
        self.clientID: str = f"{address[0]}:{address[1]}"

class whiteBoard():
    def __init__(self, size):
        self.clients = {}
        self.size = size

    def discnctClient(self, clientKey: str):
        client = self.clients.get(clientKey)
        client.connection.close()
        self.clients.pop(clientKey)

    def close(self):
        for clientKey in self.clients.keys():
            self.discnctClient(clientKey)
        print(self.clients)
    
    def addClient(self, client: clientClass):
        self.clients[client.clientID] = client
        thread.start_new_thread(whiteBoard.listnerThread, (self, client))

    def listnerThread(self, client: clientClass):
        client.connection.send("Connection accepted.".encode("utf-8"))
        while True:
            try:
                data = client.connection.recv(1024)
            except:
                self.discnctClient(client.clientID)
                break
            for otherClientKey in self.clients.keys():
                otherClient = self.clients[otherClientKey]
                if client.clientID == otherClient.clientID:
                    continue
                try:
                    otherClient.connection.send(data)
                except:
                    self.discnctClient(otherClient)


def main():
    newWhiteboard = whiteBoard(500)
    
    mainSocket = socket()
    usedPort = int(input("Port to use: "))
    mainSocket.bind(("", usedPort))
    mainSocket.listen()

    while True:
        client, address = mainSocket.accept()
        print(client, address, "Connected")
        newClient = clientClass(address, client)
        newWhiteboard.addClient(newClient)
        

        

if __name__ == "__main__":
    main()
    