import socket
import select
import sqlite3

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8080))
server_socket.listen(255)
open_client_sockets = []
adress = {}
open1={}
connection = sqlite3.connect('sqlite_A.db')
connection.row_factory = sqlite3.Row
cursor= connection.cursor()

#cursor.execute('CREATE TABLE ArieL (name TEXT PRIMARY KEY, password INTEGER)')

def log_in(name, password):
    try:
        cursor.execute('SELECT * FROM ArieL WHERE name=?', (password,))
        row = cursor.fetchone()
        password = row['password']
        name = row['name']

        print(name)
        print(password)
        return True

    except:
        return False
def register(name, password):
    try:
        cursor.execute('INSERT INTO ArieL VALUES(?,?)', (name,int(password)))
        connection.commit()
        return True
    except:
        return False

while True:
    data = ""
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
            adress[new_socket] = address
        else:
            try:
                data = current_socket.recv(4096)
                data = str(data)
                data = data[2:-1]
                print(data)
            except ConnectionResetError:
                open_client_sockets.remove(current_socket)
            if data == "":
                pass
            else:
                data = data.split("/")
                print(data)
                if(data[0]=="(register)"):
                    if register(data[1], data[2]):
                        current_socket.send(b"add")
                    else:
                        current_socket.send(b"username already taken")
                elif(data[0]=="(login)"):
                    print('hh')
                    if log_in(data[1], data[2]):
                        current_socket.send(b"login")
                    else:
                        current_socket.send(b"username or password is wrong")
                elif data[0]=="(id)":
                    open1[data[1]] = [data[2],current_socket]
                elif data[0]=="(conn)":
                        ip = open1[data[1]]
                        print('ll')
                        print(ip)
                        ip[1].send((data[2]+ " want to connect to you/"+str(adress[current_socket])).encode('utf-8'))