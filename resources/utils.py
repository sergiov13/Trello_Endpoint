import json
import requests
import random



def load_credentials():
    '''
        Handles loading the credentials from config_files/config.json,will return 
        True flag if all config values are introduced
        False flag if one or more values are missing
        This method does not verify if credentials are valid
    '''
    config_file = open("config_files/config.json")
    config = json.load(config_file)
    config_file.close()
    if config["key"] != "" and config["token"] != "" and config["board"]["id"] != "":
        key = config["key"]
        token = config["token"]
        return True, config["trello_api"], key, token, config["board"]["id"]
    else:
        return False, config["trello_api"], "", "", config["board"]


def load_session(key, token, board_id, session):
    '''
        Handles the validation of credentials and loads the session object, will return
        True if credentials are valid
        False if credentials are not valid
    '''
    try:
        user = trello_login(session.url, key, token)
        board = trello_board_from_id(session.url, key, token, board_id)
        lists = trello_lists(session.url, key, token, board_id)
    except:
        session.flag = False
        session.key = ""
        session.token = ""
        session.user = ""
        session.board = ""
        session.lists = ""
        return session
    if user != "" and board != "" :
        session.flag = True
        session.key = key
        session.token = token
        session.user = user
        session.board = board
        session.lists = lists
        return session


def trello_login(api_url, key, token):
    '''
        Handles the initial login
    '''
    user_data = {"key": key, "token": token}
    user = requests.get(url=api_url+"/members/me",params=user_data)
    return user.json()


def trello_board_from_id(api_url, key, token, board_id):
    '''
        Fetches the board
    '''
    boards_data = {
        "key": key,
        "token": token,
        "fields": "name,url,memberships,lists",
    }
    board = requests.get(url=api_url + "/boards/" + board_id, params=boards_data)
    return board.json()


def trello_lists(api_url, key, token, board_id):
    '''
        Fetches the lists if credentials are valid
    '''
    lists_params = {"key": key, "token": token}
    lists = requests.get(url=api_url + "/boards/" + board_id + "/lists", params=lists_params)
    return lists.json()


def issue(data, session):
    '''
        Handles the logic for issues that will go in list "To Do"
    '''
    params = {
    "key": session.key,
    "token": session.token,
    "name": data["title"],
    "desc": data["description"],
    "idList": get_list_id(session.lists,"to do"),
    }
    if params["idList"] != None:
        return publish_to_trello(session, params)
    else:
        return "List To Do does not exists"


def bug(data, session):
    '''
        Handles the logic for bug that will go in list "Bug"
    '''
    word_list = data["description"].split(" ")
    number = random.randint(1 ,len(data["description"]))
    word = word_list[number % len(word_list)]
    labels = check_label(session, ["bug"], "bug")
    random_member = random.randint(0, len(session.board["memberships"]) - 1)
    params ={
    "key": session.key, 
    "token": session.token,
    "name": f"bug-{word}-{number}",
    "desc": data["description"],
    "idList": get_list_id(session.lists,"bug"),
    "idLabels": labels["bug"],
    "idMembers": [session.board["memberships"][random_member]["idMember"]]
    }
    if params["idList"] != None:
        return publish_to_trello(session, params)
    else:
        return "List Bug does not exists"


def task(data, session):
    '''
        Handles the logic for task that will go in list "Task"
    '''
    category_list = ["Maintenance", "Research", "Test"]
    labels = check_label(session, category_list, data["Category"])
    params = {
    "key": session.key, 
    "token": session.token,
    "name": data["title"],
    "idLabels": "" ,
    "idList": get_list_id(session.lists,"task"),
    }
    if data["Category"] in labels.keys() and params["idList"] != None:
        params["idLabels"] = labels[data["Category"]]
        return publish_to_trello(session, params)
    else:
        return "Incorrect Category or List does not exists"


def check_label(session, labels, label):
    '''
        Handles the fetch and creation of labels or categories, 
        if the label doesn't exist in the board 
        this will create them before creating a card with that label
    '''
    label_aux = {}
    data={
        "key": session.key, 
        "token": session.token, 
        "name": label, 
        "idBoard": session.board["id"]}
    resp = requests.get(url=session.url+"/boards/"+ session.board["id"]+"/labels", params=data)
    for label in resp.json():
        if label["name"] != "":
           label_aux[label["name"]] = label["id"] 
    for label in labels:
        if label not in label_aux.keys():
            requests.post(url=session.url+"/labels",params=data)
    return label_aux


def get_list_id(lists, selection):
    '''
        Handles getting the id for the selected list
    '''
    for trello_list in lists:
        if trello_list["name"].lower() == selection:
            return trello_list["id"]
    return None

def publish_to_trello(session,params_data):
    '''
        Handles all creations of cards from previously setted parameters
    '''
    resp = requests.post(url=session.url+"/cards", params=params_data)
    return resp.json()

 