class User:

    # general data of user
    username = None

    # user socket
    socket = None

    # user session
    session = None

    def __init__(self, username, socket) -> None:
        self.username = username
        self.socket = socket