import json


def get_user_info_by_id(id: str) -> list[str, str]:
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    users_list = database_dict["users"]
    for user in users_list:
        if user["id"] == id:
            found_user = [user["username"], user["password"]]
            return found_user
    raise ValueError("User Not Found")


def get_id_by_username(username: str) -> str:
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    users_list = database_dict["users"]
    for user in users_list:
        if user["username"] == username:
            return user["id"]
    raise ValueError("User Not Found")


def authenticate(username, password):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    users_list = database_dict["users"]
    for user in users_list:
        if username == user["username"] and password == user["password"]:
            return True
    return False


def get_usernames(username):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    users_list = database_dict["users"]
    end_text = ""
    for user in users_list:
        if user["username"] != username:
            end_text += user["username"] + "\n"
    return end_text


def save_message(message, date, time):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    messages_list = database_dict["messages"]
    if messages_list == []:
        id = "1"
    else:
        id = str(int(messages_list[-1]["id"])+1)
    dict = {"id": id, "message": message, "date": date, "time": time}
    messages_list.append(dict)
    file.close()
    file = open("database.json", "w", encoding="utf-8")
    json.dump(database_dict, file, ensure_ascii=False, indent=4)
    file.close()
    return id


def save_messaging_history(sender_id, receiver_id, message_id):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    history_list = database_dict["messaging_history"]
    if history_list == []:
        id = "1"
    else:
        id = str(int(history_list[-1]["id"]) + 1)
    dict = {"id": id, "sender_id": sender_id, "receiver_id": receiver_id, "message_id": message_id}
    history_list.append(dict)
    file.close()
    file = open("database.json", "w", encoding="utf-8")
    json.dump(database_dict, file, ensure_ascii=False, indent=4)
    file.close()
    return id


def get_messaging_history(sender_id, receiver_id):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    messages = database_dict["messages"]
    users = database_dict["users"]
    history = database_dict["messaging_history"]
    chat = []
    for message_h in history:
        if message_h["receiver_id"] == receiver_id and message_h["sender_id"] == sender_id:
            message_id = message_h["message_id"]
            message = get_message_by_id(message_id)
            text = message["message"]
            date = message["date"]
            is_sent = True
            message_dict = {"message": text, "date": date, "is_sent": is_sent}
            chat.append(message_dict)
        elif message_h["receiver_id"] == sender_id and message_h["sender_id"] == receiver_id:
            message_id = message_h["message_id"]
            message = get_message_by_id(message_id)
            text = message["message"]
            date = message["date"]
            is_sent = False
            message_dict = {"message": text, "date": date, "is_sent": is_sent}
            chat.append(message_dict)
    return chat


def get_message_by_id(id):
    file = open("database.json", "r", encoding="utf-8")
    database_dict = json.load(file)
    messages = database_dict["messages"]
    for message in messages:
        if id == message["id"]:
            return message
    raise IndexError("Message Not Found")
