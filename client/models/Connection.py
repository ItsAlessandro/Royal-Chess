import socket
import pickle

class Connection:

    # Constructor
    def __init__ (self) -> None:

        # welcome port
        self.port = 8080

        # headersize of messages
        self.headersize = 10
        
        # welcome socket
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # server definitive socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # function that initializes the connection client / server
    def connect_to_server(self, server_ip : str) -> bool:

        print(f'server ip: {server_ip}')
        
        # guarantee that the user will insert a valid ip
        try:

            # test the connection
            self.welcome_socket.connect((server_ip.strip(), self.port))

            # recieving new port
            new_port = self.welcome_socket.recv(1024).decode('utf-8')

            # update the port
            self.server.connect((server_ip.strip(), int(new_port)))

            # recieving the authentication message
            while True:

                auth_message = ''
                new_message = True

                while True:
                    message = self.server.recv(16)

                    if new_message:

                        message_length = int(message[:self.headersize])
                        new_message = False
                        
                    auth_message += message.decode('utf-8')

                    if len(auth_message) - self.headersize == message_length:
                        break
                    
                print(f'full message: {auth_message}')

                if auth_message[self.headersize:] == 'Royal Chess': return True
                else: raise Exception('Invalid IP, try again.')
                
        except Exception as e:
            
            print(e)
                
            # if the connection fails, return False
            return False

    # sends a message to the server
    def send_message(self, message : str) -> str:

        # serializes the message
        message = f'{len(message):<{self.headersize}}' + message

        # sends the message
        self.server.send(bytes(message, 'utf-8'))

        print(f'inside send: {bytes(message, "utf-8")}')

        # listens the response
        response = self.server.recv(1024)

        try:
            # deserializes the response if it's a pickled object
            message = pickle.loads(response[self.headersize:])
            return message
        
        except pickle.UnpicklingError:
            # if it's not a pickled object, decode it as a string
            return response.decode('utf-8')
        
    def validate_username(self, username : str) -> bool:

        # sending the formatted message
        res = self.send_message(f'NAME:{username}')

        # if positive response return True
        if res[self.headersize:] == 'OK': return True
        else: return False

    def join_session(self, session : str):

        print('sent res')
        
        # sending the formatted message
        res = self.send_message(f'JOIN:{session}')

        print(res)

        # if positive response return True
        if res[self.headersize:].startswith('OK') : return res[self.headersize:].split(':')[1]
        else: return False

    def create_session(self, session : str) -> bool:
        
        # sending the formatted message
        res = self.send_message(f'CREATE:{session}')

        # if positive response return True
        if res[self.headersize:] == 'OK': return True
        else: return False

    def start_game(self) -> bool:

        # sending the formatted message
        res = self.send_message('START')

        # if positive response return True
        if res[self.headersize:] == 'OK': return True
        else: return False

    def listen_for_guest(self) -> str:

        print('recv from server...')

        # recieving the guest username
        guest_username = self.server.recv(1024).decode('utf-8')

        return guest_username
    
    def listen_for_start(self) -> bool:

        print('recv from server...')

        # recieving the start message
        start_message = self.server.recv(1024).decode('utf-8')

        print(f'start message: {start_message}')

        return start_message

    def listen_for_move(self) -> str:

        print('recv from server...')

        # recieving the move
        move = self.server.recv(1024).decode('utf-8')

        print(f'FROM SERVER: {move}')

        return move
    
    def send_move(self, move : str) -> bool:

        # sending the move
        res = self.send_message(move)

        # if positive response return True
        if res[self.headersize:] == 'OK': return True
        else: return False