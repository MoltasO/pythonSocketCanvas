from socket import *
import _thread as thread
import tkinter as tk


mainSocket: socket = None
root = tk.Tk()
canvas = tk.Canvas(master=root,width=500,height=450,background="Black")
canvas.grid(row=3,column=0,columnspan=2)

oldx, oldy = None, None

def reset(event):
    global oldx, oldy
    oldx = None
    oldy = None

def draw(event):
    global oldx, oldy
    global canvas
    if (oldx and oldy):
        canvas.create_line(oldx, oldy, event.x, event.y, fill="white", width=3)
        mainSocket.send(f"{oldx};{oldy};{event.x};{event.y}".encode("utf-8"))
    oldx = event.x
    oldy = event.y


canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", reset)


def revcThread():
    global mainSocket
    global canvas
    while True:
        message = mainSocket.recv(1024).decode()
        lisst = message.split(";")
        canvas.create_line(lisst[0], lisst[1], lisst[2], lisst[3], fill="white", width=3)



def connectToServer(ipAdress: str, port: int):
    global mainSocket
    mainSocket = socket()
    mainSocket.connect((ipAdress, port))

    status = mainSocket.recv(1024).decode()
    print(status)
    thread.start_new_thread(revcThread, ())
    #while True:
    #    mainSocket.send(input("Enter: message ").encode())
    #isConnected = False
    #mainSocket.close()

def main():
    global root
    root.geometry("500x500+500+500")
    ipEntry = tk.Entry(root)
    ipEntry.insert(0, "localhost")
    portEntry = tk.Entry(root)
    portEntry.insert(0, "8888")
    def connectButtonFunc():
        connectToServer(ipEntry.get(), int(portEntry.get()))


    tk.Button(root, text="Connect to server", command=connectButtonFunc).grid(row=2,column=0)
    tk.Label(root, text = 'IP address').grid(row=0,column=0)
    ipEntry.grid(row=0,column=1)
    tk.Label(root, text = 'Port').grid(row=1,column=0)
    portEntry.grid(row=1,column=1)
    
    root.mainloop()
    
        
    

if __name__ == "__main__":
    main()