import socket
import threading
import messaging_protocol as mp
import json
import datetime


def receive_messages():
    while True:
        message = socket.recv(1024)
        if message == b"":
            break
        print(message.decode())


def send_user_to_chat(socket):
    all_connectable_users = mp.recv_information(socket)[1]
    print(all_connectable_users)
    chat_request = input("With Which Person Do You Want To Talk?")
    mp.send_text(socket, chat_request)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("127.0.0.1", 8100))
for a in range(1, 4):
    try:
        file = open("cookies.json", "r", encoding="utf-8")
        cookies = json.load(file)
        file.close()
        username = cookies["username"]
        password = cookies["password"]
        date = cookies["date"].split("-")
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        date_today = datetime.date.today()
        delta = date_today - date
        last_time_login = delta.days
        if last_time_login > 14:
            raise Exception()
    except:
        username = input("What is your username?")
        password = input("What is your password?")

    mp.send_text(socket, username)
    mp.send_text(socket, password)
    accepted = mp.recv_information(socket)[1]
    if accepted == "0":
        if a == 3:
            raise ConnectionError("Authentication Failed")
    else:
        file = open("cookies.json", "w", encoding="utf-8")
        dict_to_write = {"username": username, "password": password, "date": str(datetime.date.today())}
        json.dump(dict_to_write, file, ensure_ascii=False, indent=4)
        file.close()
        break
while True:
    send_user_to_chat(socket)
    history = mp.recv_information(socket)[1]
    print(history)

    thread = threading.Thread(target=receive_messages)
    thread.start()

    while True:
        message_sent = input("")
        if message_sent == "exit":
            break
        mp.send_text(socket, message_sent)

socket.close()
