class Session:
    #Default url in case none is specified just for redundancy
    def __init__(self, flag ,key, token, user, board, lists, url= "https://api.trello.com/1"):
        self.flag = flag
        self.key = key
        self.token = token
        self.user = user
        self.board = board
        self.lists = lists
        self.url = url