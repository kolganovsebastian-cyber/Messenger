import socket
import threading
import dbhelpers
import datetime
import messaging_protocol as mp


def connect_users(socket_client, sender_username):
    all_connectable_users = dbhelpers.get_usernames(sender_username)
    mp.send_text(socket_client, all_connectable_users)
    receiver_username = mp.recv_information(socket_client)[1]
    connected_users[sender_username] = receiver_username
    return receiver_username


def send_history(socket_client, sender_username, receiver_username):
    sender_id = dbhelpers.get_id_by_username(sender_username)
    receiver_id = dbhelpers.get_id_by_username(receiver_username)
    messaging_history = dbhelpers.get_messaging_history(sender_id, receiver_id)
    history = ""
    for message in messaging_history:
        text = ""
        if message["is_sent"] is True:
            text += " " * 10
        text += f"{message["date"]} : {message["message"]}\n"
        history += text
    mp.send_text(socket_client, history)


def save_message_to_history(received, sender_username, receiver_username):
    time = str(datetime.datetime.now().time())
    date = str(datetime.date.today())
    message_id = dbhelpers.save_message(received, date, time)
    sender_id = dbhelpers.get_id_by_username(sender_username)
    receiver_id = dbhelpers.get_id_by_username(receiver_username)
    dbhelpers.save_messaging_history(sender_id, receiver_id, message_id)


def get_message(socket_client):
    sender_username = check_client(socket_client)
    if sender_username is None:
        return None
    while True:
        receiver_username = connect_users(socket_client, sender_username)
        send_history(socket_client, sender_username, receiver_username)
        while True:
            received = mp.recv_information(socket_client)[1]
            if received == "" or received == "exit":
                break
            if receiver_username in connected_users:
                if connected_users[receiver_username] == sender_username:
                    mp.send_text(all_clients[receiver_username], received)
            save_message_to_history(received, sender_username, receiver_username)


def check_client(socket_client):
    for a in range(1, 4):
        username = mp.recv_information(socket_client)[1]
        password = mp.recv_information(socket_client)[1]
        if dbhelpers.authenticate(username, password):
            mp.send_text(socket_client, "1")
            all_clients[username] = socket_client
            return username
        else:
            mp.send_text(socket_client, "0")


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("0.0.0.0", 8100))
socket.listen()


all_clients = {}
connected_users = {}


while True:
    connection_list = socket.accept()
    socket_client = connection_list[0]
    address = connection_list[1]
    print(f"connected by {address}")
    thread = threading.Thread(target=get_message, args=[socket_client])
    thread.start()

socket.close()
