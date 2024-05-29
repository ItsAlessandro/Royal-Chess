class Session:

    # unique string of session
    session_id = None

    # players
    host = guest = None

    # game state
    started = False

    def __init__(self, session_id, host) -> None:
        self.session_id = session_id
        self.host = host