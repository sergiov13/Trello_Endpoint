import logging
from flask import Flask, request, render_template
from resources.utils import load_credentials,  issue, bug, task, load_session
from resources.session import Session


LOG = logging.getLogger(__name__)
app = Flask(__name__)


'''
    Handles the routing to create cards and verifies log in before creating a card
'''
@app.route('/', methods=['GET','POST'])
def routing():
    if request.method == 'POST' and session.flag:
        data = request.get_json()
        if data["type"].lower() == "issue":
            return issue(data, session)
        elif data["type"].lower() == "bug":
            return bug(data, session)
        elif data["type"].lower() == "task":
            return task(data, session)
    elif request.method == 'GET' and session.flag:
        return "Hello "+ session.user["fullName"]
    elif session.flag == False:
        return '''Welcome you need to head to http://localhost:3000/login in your browser to enter your credentials,
or send a json POST request to that link with pairs:
{"key":<trello_key>,"token":<trello_token>,"board_id":<board_id>}'''

'''
    Will handle the login if credentials are not found in config file
'''
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        if request.form:
            load_session(request.form['key'], request.form['token'], request.form['board_id'], session)
            return "Welcome "+ session.user["username"] + " to board " + session.board["name"] if session.flag else "Wrong Credentials"
        else:
            data = request.get_json()
            try:
                load_session(data["key"], data["token"], data["board_id"], session)
            except:
                return "Missing Credential or incorrect key"
            return "Welcome "+ session.user["username"] + " to board " + session.board["name"] if session.flag else "Wrong Credentials"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    LOG.info("Using flask as WSGI server")
    LOG.info("Starting server")
    
    LOG.info("Loading Trello Credentials")

    #Loads Credentials from Config, Credentials Flag will be True if Config File has data
    credentials_flag, url, cred_key, cred_token, cred_board_id = load_credentials() 

    #Creates empty session object
    #Session(flag, key, token, user, board, lists, url)
    session = Session(False, "", "","","", url)

    if credentials_flag:
            #load_session(url, key, token, board_id, session)
            session = load_session(cred_key, cred_token, cred_board_id, session)
            LOG.info("Logged in Succesfully as "+ session.user["fullName"] + " in board" + session.board["name"] if session.flag else "Wrong Credentials")
    else:
        LOG.info("Login Credentials not found in Config File or incorrect")

    app.run(host="0.0.0.0", port=3000, threaded=False)


