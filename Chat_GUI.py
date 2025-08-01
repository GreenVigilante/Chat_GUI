import socket
import threading
import tkinter as tk
import tkinter.scrolledtext
from tkinter import simpledialog
import time
host = "0.tcp.in.ngrok.io"
port = 14339

dialog = tk.Tk()
dialog.withdraw()
nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=dialog)

running = True

yappers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
yappers.connect((host, port))
def recieve():
    global running
    while running:
        try:
            message = yappers.recv(1024).decode("ascii")
            if message == "Nickname: ":
                yappers.send(nickname.encode("ascii"))
                admin_mess = yappers.recv(1024).decode("ascii")
                if admin_mess == "adminjumpsin":
                    yappers.send(password.encode("ascii"))
                    if yappers.recv(1024).decode("ascii") == "NO":
                        text_area.config(state= "normal")
                        text_area.insert("end", "You ain't no admin!\n")
                        text_area.yview("end")
                        text_area.config(state="disabled")
                        time.sleep(2)
                        stop_it()
                    else:
                        text_area.config(state= "normal")
                        text_area.insert("end", "Hola admin. Who we harrassing today?\n")
                        text_area.yview("end")
                        text_area.config(state="disabled")
                elif admin_mess == "BAN":
                    text_area.config(state= "normal")
                    text_area.insert("end", "You have been banned ;)\n")
                    text_area.yview("end")
                    text_area.config(state="disabled")
                    time.sleep(2)
                    stop_it()
                elif admin_mess == "CHOOSEN":
                    text_area.config(state= "normal")
                    text_area.insert("end", "Name already been choosen :)\n")
                    text_area.yview("end")
                    text_area.config(state="disabled")
                    time.sleep(2)
                    stop_it()
            else:
                text_area.config(state= "normal")
                text_area.insert("end", message)
                text_area.yview("end")
                text_area.config(state="disabled")
        except:
            text_area.config(state= "normal")
            text_area.insert("end", "An error has occured boomer\n")
            text_area.yview("end")
            text_area.config(state="disabled")
            time.sleep(2)
            stop_it()

def stop_it():
    global running
    running = False
    win.destroy()
    yappers.close()
    exit(0)

def write():
    message = f"""{nickname}: {input_box.get("1.0", "end")}"""
    if message[len(nickname)+2:].startswith("/"):
        if nickname == "admin":
            if message[len(nickname)+2:].startswith("/ban"):
                yappers.send(f"ban {message[len(nickname)+2+5:-1]}".encode("ascii"))
                input_box.delete("1.0", "end")
            elif message[len(nickname)+2:].startswith("/kick"):
                yappers.send(f"kick {message[len(nickname)+2+6:-1]}".encode("ascii"))
                input_box.delete("1.0", "end")
        else:
            text_area.config(state= "normal")
            text_area.insert("end", "You aint no admin boomer\n")
            text_area.yview("end")
            text_area.config(state="disabled")
            
    elif message == f"{nickname}: \n":
        pass
    elif message == f"{nickname}: exit()":
        input_box.delete("1.0", "end")
        stop_it()
    else:
        yappers.send(message.encode("ascii"))
        input_box.delete("1.0", "end")

def write_enter():
    message = f"""{nickname}: {input_box.get("1.0", "end")}"""
    message = message[:-1]
    if message[len(nickname)+2:].startswith("/"):
        if nickname == "admin":
            if message[len(nickname)+2:].startswith("/ban"):
                yappers.send(f"ban {message[len(nickname)+2+5:-1]}".encode("ascii"))
                input_box.delete("1.0", "end")
            elif message[len(nickname)+2:].startswith("/kick"):
                yappers.send(f"kick {message[len(nickname)+2+6:-1]}".encode("ascii"))
                input_box.delete("1.0", "end")
        else:
            text_area.config(state= "normal")
            text_area.insert("end", "You aint no admin boomer\n")
            text_area.yview("end")
            text_area.config(state="disabled")
            
    elif message == f"{nickname}: \n":
        pass
    elif message == f"{nickname}: exit()\n":
        input_box.delete("1.0", "end")
        stop_it()
    else:
        yappers.send(message.encode("ascii"))
        input_box.delete("1.0", "end")

if nickname == "admin":
    dialog_pass = tk.Tk()
    dialog_pass.withdraw()
    password = simpledialog.askstring("Password", "Please enter Password", parent=dialog_pass)

win = tk.Tk()
win.config(bg="lightgray")
Chat_label = tk.Label(win, text="Chat GUI", bg= "lightgray")
Chat_label.config(font=("Arial", 12))
Chat_label.pack(padx=20, pady=5)

text_area = tkinter.scrolledtext.ScrolledText(win)
text_area.pack(padx=20, pady= 5)
text_area.config(state="disabled")
msg_label = tk.Label(win, text="Messages:", bg= "lightgray")
msg_label.config(font=("Arial", 12))
msg_label.pack(padx=20, pady=5)
input_box = tk.Text(win, height= 3)
input_box.pack(padx=20, pady=5)
send_btn = tk.Button(win, text="Send", command=write)
send_btn.config(font=("Arial", 12))
send_btn.pack(padx=20, pady=5)
win.bind("<Return>", lambda event: write_enter())
win.protocol("WM_DELETE_WINDOW", stop_it)
tr = threading.Thread(target=recieve)
tr.start()
win.mainloop()