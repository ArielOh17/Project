from tkinter import *
from tkinter import messagebox
import socket
from PIL import ImageGrab, ImageTk  # this libary take a image from the desktop
import threading
from PIL import Image
import pygame
from pygame.locals import *
import autopy
from pynput.mouse import Controller
from pynput.mouse import Button as Button2
import keyboard

hostname = socket.gethostname()
myp = socket.gethostbyname(hostname)   # get's the computer ip.
global background

# Name: Ariel Ohev
# input: none
# output: create the main window of the program with the logo of the program and option to login or register account.
class Main_page:
    def __init__(self, master):
        master.geometry("400x450")
        master.resizable(0, 0)
        base = Frame(master, bg="grey95")
        base.pack(expand=True, fill='both')
        a = Label(base, text="AViewer", bg="grey20", width="200", height="2", foreground="white", font=("arial", 15))
        a.pack()
        a = Label(base, bg="grey95", width="10", height="1", foreground="white", font=("arial", 15))
        a.pack()
        self.log = Button(base, relief=FLAT, borderwidth=4, text="Log-in", bg="grey80", width="20", height="2",
                          font=("arial", 12), command=lambda: self.move_page(base, master, name="login"))
        self.log.pack()
        a = Label(base, bg="grey95", width="20", height="1")
        a.pack()
        self.reg = Button(base, relief=FLAT, borderwidth=4, text="Register", bg="grey80", width="20", height="2",
                          font=("arial", 12), command=lambda: self.move_page(base, master, "pp"))
        self.reg.pack()
        self.background = ImageTk.PhotoImage(file= "logo3.png")
        back1 = Label(base, image=self.background)
        back1.place(x=120, y=250)
    def move_page(self, base, master, name="login"):
        base.destroy()
        if name == "login":
            LogIN(master)
        else:
            Register(master)


# Name: Ariel Ohev
#input: none
#ouput: create the option to create a new account.
class Register:
    def __init__(self, master):
        master.geometry("400x450")
        master.resizable(0, 0)
        base1 = Frame(master, bg="grey95")
        base1.pack(expand=True, fill="both")
        base2 = Frame(base1, bg="grey95")
        base2.pack(expand=True, fill="both")
        base = Frame(base1, bg="grey95")
        base.pack(expand=True, fill="both")
        self.b_m = [base1, master]
        a = Label(base2, text="AViewer", bg="grey20", width="200", height="2", foreground="grey95", font=("arial", 15))
        a.pack()

        self.reg = Button(base1, relief=FLAT, borderwidth=1, text="Go back", width="6", height="1", foreground="grey95",
                          font=("arial", 11), command=lambda: self.move_page(base1, master), bg="grey20")
        self.reg.place(x=10, y=10)

        Label(base, text="Please enter detail below", font=("arial", 15), bg="grey95").pack()
        Label(base).pack()

        Label(base, text="User Name: ", font=("arial", 12), bg="grey95").pack()
        self.Password_Box1 = Entry(base, font=("arial", 12), relief=GROOVE, borderwidth=4)
        self.Password_Box1.pack()
        Label(base, text="Password: ", font=("arial", 12), bg="grey95").pack()
        self.Password_Box2 = Entry(base, font=("arial", 12), show="*", relief=GROOVE, borderwidth=4)
        self.Password_Box2.pack()
        Label(base, text="Reenter Password: ", font=("arial", 12), bg="grey95").pack()
        self.Password_Box3 = Entry(base, font=("arial", 12), show="*", relief=GROOVE, borderwidth=4)
        self.Password_Box3.pack()
        a = Label(base, bg="grey95", width="10", height="1", foreground="grey95", font=("arial", 15))
        a.pack()
        self.reg = Button(base, relief=GROOVE, borderwidth=4, text="Register", width="20", height="2",
                          font=("arial", 11), command=lambda: self.save())
        self.reg.pack()
        self.Password_Box1.bind("<Key>", self.next1)
        self.Password_Box2.bind("<Key>", self.next2)
        self.Password_Box3.bind("<Key>", self.next3)


    #input: none
    #output: part of the option to move line by pressing enter.
    def next1(self, e):
        if e.char == "\r":
            self.Password_Box2.focus()

    # input: none
    # output: part of the option to move line by pressing enter.
    def next2(self, e):
        if e.char == "\r":
            self.Password_Box3.focus()

    # input: none
    # output: part of the option to move line by pressing enter.
    def next3(self, e):
        if e.char == "\r":
            f = self.save()

    # input: none
    # output: part of the option to move line by pressing enter.
    def move_page(self, base, master, name="login"):
        base.destroy()
        Main_page(master)

    #Name: Ariel Ohev
    #input: none
    #output: sending the information of the man that create a new account and senf it to the server so he could save it on the data base.
    def save(self):
        u = self.Password_Box1.get()
        p = self.Password_Box2.get()
        pp = self.Password_Box3.get()
        if p != pp:
            messagebox.showerror("ERROR", "password not same")
            return False
        my_socket.send(("(register)/" + u + "/" + p).encode('utf-8'))

        data = my_socket.recv(4096)
        data = str(data)
        data = data[2:-1]
        if data == "add":
            self.move_page(self.b_m[0], self.b_m[1])
            return True
        messagebox.showerror("ERROR", "user name already taken")
        return False



#Name: Ariel Ohev
#input: none
#output: create the login window and cheking by the server if the information are correct and moving to the other page.
class LogIN:
    def __init__(self, master):
        master.geometry("400x450")
        master.resizable(0, 0)
        base1 = Frame(master)
        base1.pack()
        base2 = Frame(base1)
        base2.pack()
        base = Frame(base1)
        base.pack(expand=True)
        self.b = base1
        self.m = master
        a = Label(base2, text="AViewer", bg="grey20", width="200", height="2", foreground="white", font=("arial", 15))
        a.pack()
        a2 = Label(base, bg="grey95", width="200", height="1", foreground="white", font=("arial", 15))
        a2.pack()
        self.reg = Button(base1, relief=FLAT, borderwidth=1, text="Go back", width="6", height="1", foreground="grey95",
                          font=("arial", 11), command=lambda: self.move_page(base1, master), bg="grey20")
        self.reg.place(x=10, y=10)
        Label(base, text="Please enter detail below", font=("arial", 15)).pack()
        Label(base).pack()

        Label(base, text="User Name: ", font=("arial", 12)).pack()
        self.Password_Box1 = Entry(base, font=("arial", 12), relief=GROOVE, borderwidth=4)
        self.Password_Box1.pack()
        Label(base, text="Password: ", font=("arial", 12)).pack()
        self.Password_Box2 = Entry(base, font=("arial", 12), show="*", relief=GROOVE, borderwidth=4)
        self.Password_Box2.pack()
        a = Label(base, bg="grey95"
                           ""
                           "", width="10", foreground="white", font=("arial", 15))
        a.pack()
        self.reg = Button(base, relief=GROOVE, borderwidth=4, text="log in", width="20", height="2",
                          font=("arial", 13), command=lambda: self.save())
        self.reg.pack()
        self.Password_Box1.bind("<Key>", self.next1)
        self.Password_Box2.bind("<Key>", self.next2)

    def next1(self, e):
        if e.char == "\r":
            self.Password_Box2.focus()

    def next2(self, e):
        if e.char == "\r":
            f = self.save()

    def move_page(self, base, master, name="login"):
        self.b.destroy()

        if name == "o":
            host(master)
        else:
            Main_page(master)

    def save(self):
        global my_name
        u = self.Password_Box1.get()
        p = self.Password_Box2.get()
        my_socket.send(("(login)/" + u + "/" + p).encode('utf-8'))

        data = my_socket.recv(4096)
        data = str(data)
        data = data[2:-1]
        if data == "login":
            self.move_page(self.b, self.m, name='o')
            my_name = u
            return True

        messagebox.showerror("ERROR", "username or password is wrong")
        return False



#Name: Ariel Ohev
#input: none
#output: showing the user id and from this page the users can make the conncetion between them.
class host:
    def __init__(self, master):
        master.geometry("400x450")
        master.resizable(0, 0)

        base = Frame(master)
        base.pack(expand=True, fill="both")

        a = Label(base, text="AViewer", bg="grey20", width="200", height="2", foreground="white", font=("arial", 15))
        a.pack()
        a = Label(base, bg="grey95", width="10", height="1", foreground="white", font=("arial", 15))
        a.pack()
        v = self.makeid(myp)
        my_socket.send(("(id)/" + v + "/" + myp).encode('utf-8'))
        a = Label(base, text="Your id:", width="200", height="2", foreground="black", font=("arial", 15))
        a.pack()

        a = Label(base, text=v, width="200", height="2", foreground="black", font=("arial", 15))
        a.pack()
        self.Password_Box1 = Entry(base, font=("arial", 12), relief=GROOVE, borderwidth=4)
        self.Password_Box1.place(x=100, y=200)
        self.send = Button(base, relief=GROOVE, borderwidth=4, text="connect", width="10", height="1",
                           command=self.conn,
                           font=("arial", 11))
        self.send.place(x=100, y=230)
        threading.Thread(target=self.agree_conn).start()
        threading.Thread(target=lambda: self.my_server(base, master)).start()

    def move_page(self, b, m, c, s):
        b.destroy()
        server1(c, s, m)

    #Name: Ariel Ohev
    #input: none
    #output:
    def agree_conn(self):
        global root
        a = True
        while a:
            d = my_socket.recv(4096)
            d = str(d)
            d = d[2:-1]
            d = d.split("/")
            MsgBox = messagebox.askquestion('connect', str(d[0]))
            if MsgBox == 'yes':
                a = False
                print(d[1])
                client1(d[1])
            else:
                print("okey")

    def conn(self):
        my_socket.send(("(conn)/" + self.Password_Box1.get() + "/" + my_name).encode('utf-8'))


#Name: Ariel Ohev
#input: ip
#output: encrypt the ip so nobody can now what's the other ip is.
    def makeid(self, add):
        id = ""
        i = 0
        b = -1
        length = len(add)
        print(length)
        flag = True
        l = 0
        while len(id) < length:

            if length % 2 == 0:
                flag = True
            else:
                flag = False

            if add[i].isdigit():
                id += add[i]
                l = l + 1

            if l == 3 and add[i].isdigit() == False:
                id += ""

            if l == 3:
                id += "."
                l = 0

            if len(id) == length and flag == False:
                break

            if add[b].isdigit():
                id += add[b]
                l = l + 1

            if l != 3 and add[i].isdigit() == False:
                id += ""

            if l == 3:
                id += "."
                l = 0

            i = i + 1
            b = b - 1
            print(l)
            print(id)

        print(id)
        return id


#Name: Ariel Ohev
#input: ip
#output: make a server so the client's can make a peer to peer connection.
    def my_server(self, b, m):
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 8082))
        server_socket.listen(100)
        conn = server_socket.accept()
        print(conn)
        self.move_page(b, m, conn, server_socket)


#Name: Ariel Ohev
#input: ip
#output: connect to the server and make a peer to peer connection between client's.
class client1:
    def __init__(self, addr):
        print('client')
        print(addr)
        addr = str(addr)
        addr = addr[1:-1]
        addr = addr.split(",")
        my_client[0] = addr[0][1:-1]
        print(my_client[0])
        my_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket2.connect((addr[0][1:-1], 8081))
        my_client[1] = my_socket2
        root.destroy()


class server1:
    def __init__(self, conn, ser, m):
        my_sever[0] = conn
        my_sever[1] = ser
        root.destroy()


#Name: Ariel Ohev
#input: string
#checking if the string is send and start taking a screen image and send it by sockets.
def screenss(name):
    if name == "send":
        print("start")
        while True:
            im = ImageGrab.grab()
            im = im.resize((800, 500), Image.ANTIALIAS)
            im.save("screen1.png", quality=1024)
            im = open("screen1.png", "rb")
            r_im = im.read()
            im.close()
            my_client[1].sendall(r_im)

#Name: Ariel Ohev
#input: None
#output: getting the mouse information and keyboard information and call the setmousevalues.
def keys():
    print("recv")
    while True:
        a = my_client[1].recv(4096)
        print(a.decode())
        a = str(a)
        a = a[2:-1]
        a = a.split(",",4)
        print(a)
        setMouseValues(a[4], a[0], a[1], a[2], a[3])

#Name: Ariel Ohev
#input: mouse information and keyboard information
#output: move the cursur of the mouse and preesing the mouse and pressing the keyboard.
def setMouseValues(ch, X, Y, LB, RB):

        autopy.mouse.move(int(X),int(Y))

        if int(LB) ==1:
            m.click(Button2.left, 1)
        if int(RB) ==1:
            m.click(Button2.right, 1)

        if ch != 'None' and len(ch)< 10:
            keyboard.press_and_release(ch)


my_sever = ["conn", "ser"]# by this string's the program can know who's the server.
my_client = ["addr", "soc"]# by this string's the program can know who's the client.
my_name = ""
m = Controller()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myp = '192.168.1.174'
my_socket.connect(('192.168.56.1', 8080))
root = Tk()
root.title("AViewer")
Main_page(root)
root.mainloop()
print(my_sever)
print(my_client)
screen = ""
if my_client[0] == "addr":
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    done = False
    c = pygame.time.Clock()
    while not done:
        (ch, LB, RB) = ('None', 0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    done = True
                else:
                    print(pygame.key.name(event.key))
                    ch = pygame.key.name(event.key)             #getting the keyboard char pressed by pygame.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("in mousebuttondown")
                print("mouse  : %d" % event.button)
                if event.button == 1:                           #check if the mouse button pressed.
                    LB = 1
                elif event.button == 3:
                    RB = 1
        (X, Y) = pygame.mouse.get_pos()                         #getting the mouse cursur position.
        mouse_data = "%d,%d,%d,%d" % (X, Y, LB, RB)
        all_data = mouse_data + "," + str(ch)
        print(all_data)
        my_sever[0][0].send(all_data.encode('utf-8'))           #send the mouse information and keyboard information
        d = my_sever[0][0].recv(40960000)                       #getting the photo of the screen and show's it on the pygame window.
        try:
            myfile = open("screen.png", 'wb')
            myfile.write(d)
            myfile.close()
            img = Image.open("screen.png")
            img = img.resize((800, 500), Image.ANTIALIAS)
            img.save("screen.png")
        except:
            pass
        try:
            img2 = pygame.image.load("screen.png")
        except:
            img2 = pygame.image.load("white.png")
        screen.blit(img2, (0, 0))
        pygame.display.flip()
        #os.remove("screen.png")
        c.tick(30)

else:
    threading.Thread(target=lambda: screenss("send")).start()   #call the function that getting the screen image by threading.
    threading.Thread(target=lambda: keys()).start()             #call the function that applies the mouse information and keyboard information on the computer.
