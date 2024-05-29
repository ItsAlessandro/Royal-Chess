import socket
import threading
import pickle

# imported models to shorten single file server usage
# else available in /models directory

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

# ip taker ------------------------------------------ #

# function to get the local ip address of the server
def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except: 
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# constants ---------------------------------------- #

# server socket creation (IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# local ip
LOCAL_IP = get_local_ip()

# server port
PORT = 8080

# next port
next_port = 8081

# header for messages
HEADERSIZE = 10

# global collection of active clients [user]
clients = []

# global collection of active sessions [session]
sessions = []

# locks
clients_lock = threading.Lock()
sessions_lock = threading.Lock()

# network functions -------------------------------- #

# function to initialize the server
def initialize_server():

    # binds the server to the local ip and port
    server.bind((LOCAL_IP, PORT))

    # listens for incoming connections
    server.listen(6)

    # prints the server address
    print(f"Server running on {LOCAL_IP}:{PORT}")

# function to send a message to a client
def send_message(socket, message):

    if type(message) != bytes:

        # serializes the message
        message = f'{len(message):<{HEADERSIZE}}' + message

        # sends the message
        socket.send(bytes(message, 'utf-8'))

    # already in bytes
    else:
            
            message = bytes(f'{len(message):<{HEADERSIZE}}', 'utf-8') + message
            
            # sends the message
            socket.send(message)

# client handling functions ------------------------ #

# function to return a client by username
def get_client(username : str):

    # iterates through all active clients
    for client in clients:

        # if user exists returns the tuple [user, socket]
        if client.username == username:
            return client
        
    # if user does not exist returns False
    return False

# function to return a session by session_id
def get_session(session_id : str):

    # iterates through all active sessions
    for session in sessions:

        # if session exists returns the session
        if session.session_id == session_id:
            return session
        
    # if session does not exist returns False
    return False


# function to handle the client
def client_handler(welcome_socket, welcome_address, new_port):

    global socket

    # creating new socket
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((LOCAL_IP, new_port))
    s_socket.listen(1)

    # sending the new port to the client
    welcome_socket.send(bytes(f'{new_port}', 'utf-8'))

    # accepting the new connection
    session_socket, session_address = s_socket.accept()

    # closing the welcome socket
    welcome_socket.close()

    # current user object
    user = None
    
    # initial authentication
    send_message(session_socket, 'Royal Chess')

    try:

        # listening loop
        while True:

            full_message = ''
            new_message = True

            # message receiving loop
            while True:

                message = session_socket.recv(16)

                # if is a new message, picks up the header
                if new_message:
                    message_length = int(message[:HEADERSIZE])
                    new_message = False

                full_message += message.decode('utf-8')

                # if the message is complete, breaks the loop
                if len(full_message) - HEADERSIZE == message_length:
                    
                    # resetting the message variables
                    new_message = True
                    break

            print(f'DEBUG: full message received={full_message}')

            # start the current session
            if full_message[HEADERSIZE:].split(':')[0] == 'START':

                    sessions_lock.acquire()

                    # if the user is the host of the session
                    if user and user.session.host == user:

                        # if the session if full of players
                        if user.session.guest:

                            # communicate the session startup
                            send_message(user.session.guest.socket, 'START')

                            # starting the session
                            user.session.started = True

                            # console log of the started session
                            print(f'{session_address} started session {user.session.session_id}')

                            # sends the start message
                            send_message(session_socket, 'OK')

                        # session not full
                        else:
                            send_message(session_socket, 'FORBIDDEN')

                    # if the user is not the host
                    else:
                        send_message(session_socket, 'FORBIDDEN')

                    sessions_lock.release()

            # asking to join a session "JOIN:session_id"
            if full_message[HEADERSIZE:].split(':')[0] == 'JOIN':

                        sessions_lock.acquire()

                        # chosen session id
                        session_id = full_message[HEADERSIZE:].split(':')[1]

                        # chosen session 
                        session = get_session(session_id)

                        # if the session exists
                        if session:
                                
                                # if the session is not full of players
                                if not session.guest and user != None:
            
                                    # sets the user as the guest of the session
                                    session.guest = user

                                    # setting the user session
                                    user.session = session
            
                                    # console log of the joined session
                                    print(f'{session_address} joined session {session_id}')

                                    send_message(session.host.socket, 'JOINED:' + user.username)
            
                                    send_message(session_socket, f'OK:{session.host.username}')
            
                                # if the session is started
                                else:
                                    send_message(session_socket, 'FORBIDDEN')
                        
                        else:
                            send_message(session_socket, 'NOTFOUND')

                        sessions_lock.release()

            # asking all the avaialble sessions "GET"
            if full_message[HEADERSIZE:] == 'GET':
                            
                            if user:
                                # list of all available sessions
                                available_sessions = []
                
                                # iterates through all active sessions
                                for session in sessions:
                
                                    # if the session is not started
                                    if not session.started:
                
                                        # appends the session to the list
                                        available_sessions.append(session.session_id)
                
                                # sends the list of available sessions
                                send_message(session_socket, pickle.dumps(available_sessions))
                            
                            else:
                                # user does not exist
                                send_message(session_socket, 'FORBIDDEN')

            # deleting a session "DELETE:session_id"
            if full_message[HEADERSIZE:].split(':')[0] == 'DELETE':

                        sessions_lock.acquire()

                        # chosen session id
                        session_id = full_message[HEADERSIZE:].split(':')[1]

                        # if the session exists
                        if get_session(session_id):

                            # if the session is not started
                            if not get_session(session_id).started:

                                # if the user is the host of the session
                                if get_session(session_id).host == user:

                                    # console log of the deleted session
                                    print(f'{session_address} deleted session {session_id}')

                                    # removes the session
                                    sessions.remove(get_session(session_id))

                                    send_message(session_socket, 'OK')

                            # if the session is started
                            else:
                                send_message(session_socket, 'FORBIDDEN')

                        sessions_lock.release()

            # creating a new session "CREATE:session_id"
            if full_message[HEADERSIZE:].split(':')[0] == 'CREATE':

                        sessions_lock.acquire()
                        
                        # chosen session id
                        session_id = full_message[HEADERSIZE:].split(':')[1]

                        # if the session already exists
                        if get_session(session_id):
                            send_message(session_socket, 'CONFLICT')

                        # if user doesn't exist
                        if not user:
                            send_message(session_socket, 'FORBIDDEN')

                        # if the session does not exist
                        else:

                            # creating the new session
                            session = Session(session_id, user)
                            sessions.append(session)

                            # setting the user session
                            user.session = session

                            # console log of the new session
                            print(f'{session_address} created session {session_id}')

                            send_message(session_socket, 'OK')

                        sessions_lock.release()

            # setting the user name "NAME:username"
            if full_message[HEADERSIZE:].split(':')[0] == 'NAME':

                        clients_lock.acquire()

                        # chosen username
                        username = full_message[HEADERSIZE:].split(':')[1]

                        # if the user already exists
                        if get_client(username):
                            send_message(session_socket, 'CONFLICT')
                            
                        # if the user does not exist
                        else:

                            # if user already exists, only update the name
                            if user:
                                user.username = username

                                # console log of the updated user
                                print(f'{session_address} updated username to {username}')
                            
                            # if user does not exist, create a new user
                            else:

                                user = User(username, session_socket)
                                clients.append(user)

                                # console log of the new user
                                print(f'{session_address} connected as {username}')

                            send_message(session_socket, 'OK')

                        clients_lock.release()

            # setting a new move "MOVE:host:move"
            if full_message[HEADERSIZE:].split(':')[0] == 'MOVE':
                
                # parsing the message
                who = full_message[HEADERSIZE:].split(':')[1]
                move = full_message[HEADERSIZE:].split(':')[2]

                if who == 'host':
                    send_message(user.session.guest.socket, f'MOVE:{move}')
                    send_message(user.session.host.socket, f'OK')
                else:
                    send_message(user.session.host.socket, f'MOVE:{move}')
                    send_message(user.session.guest.socket, f'OK')
    
    # forced disconnection
    except Exception as e:

        # prints the disconnection
        print(f'{session_address} disconnected for {e}')

        # if client exists remove from clients
        if user: clients.remove(user)

        # unlocks all the locks if they are locked
        if clients_lock.locked(): clients_lock.release()
        if sessions_lock.locked(): sessions_lock.release()

# main server loop --------------------------------- #

initialize_server()

while True:

    # handshake with client
    client_socket, client_address = server.accept()

    # prints the client address
    print(f'Connection from {client_address}')

    # updating next port
    next_port += 1

    # creating the client thread
    client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address, next_port))

    # starting the client thread
    client_thread.start()