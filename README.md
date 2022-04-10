# Trello Endpoint Challenge
This is an endpoint to add Trello cards to a specified board.
We are assuming the Lists "To Do", "Bug", "Task" already exist in the Trello Board.
Currently there is only the functionality for one account to be used, and all cards will be created through this user. This could be fixed with cookies or server side sessions creating instances for every new connection, allowing for multiple users.

## Creating and running Local Environment

*Dependencies:*
    **Python3.9** \\
    **pipenv** \\
    **flask** \\
    **requests** 

First we need to install pipenv if not installed this will handle our virtual environment and install dependencies. From terminal while being inside the project folder we run the command:
```
    pip install pipenv
```
Once finished well created the virtual enviroment:
```
    pipenv shell
```
After we have our virtual enviroment created will install dependencies specified in pipfile, this will create out pipfile.lock.
```
    pipenv install
```
Finally to run the server and make the endpoint live we run the command:
```
    python3 app.py
```
To Close it just press Ctrl-C


## Creating and running Dockerfile 
You'll need to have Docker installed.

while standing in the root project folder run:
```
    docker-compose build
```
Once finished building the container run the command:
```
    docker-compose start
```
To Close it just press Ctrl-C

*NOTE*: If the config_file is changed in order for those changes to take effect we must first bring down the container if its running and rebuild it.

## Loggin in

**Configuration**
Inside the folder config_files we have the file config.json that can store the key, token and board_id. Keep in mind this will remain visible. Changes to this file will only take effect when the server is started.

**Browser**
From a browser the endpoint http://localhost:3000/login will provide us with a form where we can input the Key, Token and Board_Id

**POST Request**
We can directly log in if we send a POST request through cURL 
```
    curl -X POST -H "Content-Type: application/json" \                           
    -d '{"key":"<KEY>","token":"<TOKEN>","board_id":"<BOARD_ID>"}' \
    http://localhost:3000/login
```

**Verify Log in**
Once Logged in we can verify we are logged in and the user, if we send a get request to http://localhost:3000, if not logged in it will trow a message prompting you to log in using the browser or post request.


## Issue 
This represents a business feature that needs implementation, they will provide a short title and a description. All issues gets added to the “To Do” list as unassigned
```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"type":"issue", "title": "send Message", "description":"Let pilots send messages to Central"}' \
    http://localhost:3000
```


## Bug 
This represents a problem that needs fixing. They will only provide a description, the title needs to be randomized with the following pattern: bug-{word}-{number}. It doesn't matter that they repeat internally. The bugs should be assigned to a random member of the board and have the “Bug” label.
```
    curl -X POST -H "Content-Type: application/json" \
    -d '{"type":"bug", "description":"Cockpit is not depressurizing correctly"}' \
    http://localhost:3000
```


## Task
This represents some manual work that needs to be done. It will count with just a title and a category (Maintenance, Research, or Test) each corresponding to a label in trello. 
```
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"type": "task", "title": "Clean the Rocket", "Category":"Maintenance"`}'
    http://localhost:3000
```

If the card was created succesfully it will return the json response from trello with the card info
