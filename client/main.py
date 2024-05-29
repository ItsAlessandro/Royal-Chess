import pygame
import sys
import threading
import models.Connection as Connection
import models.pygame.Button as Button
import models.pygame.Textbox as Textbox
import models.pygame.Chessboard as Chessboard
import models.engine.engine as Engine

# pygame init
pygame.init()
pygame.display.set_caption("Royal Chess")

# network constants ------------------------------- #

connection = Connection.Connection()

# pygame constants -------------------------------- #

# screen size
WIDTH, HEIGHT = 1280, 720

# frame rate
FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (104, 72, 148)
DIRTY_WHITE = (251, 252, 228)

# images and logos
BACKGROUND = pygame.transform.scale(pygame.image.load('resources/images/background.jpg'), (WIDTH, HEIGHT))
LOGO_IMAGE = pygame.image.load('resources/images/logo_image.png')
LOGO = pygame.image.load('resources/images/logo.png')
BUTTON_BACKGROUND = pygame.image.load('resources/images/button_background.png')

# buttons lengts
button_width = 250
button_height = button_width /2.6

# fonts
FONT = pygame.font.Font('resources/fonts/aansa.ttf', 40)

# screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# user inserted variables ------------------------- #

# server ip
server_ip = ''

# username
username = ''

# session id
session_id = ''

# lobby listening
host_username, guest_username, host_started = '', '', False

# move
understood_move = ''

# pygame functions -------------------------------- #

# function that initializes the main menu
def main_menu () -> None:

    # button initialization
    play_button = Button.Button(WIDTH/2 -250/2, 415, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Play')
    help_button = Button.Button(WIDTH/2 -250/2, 505, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Credits')
    quit_button = Button.Button(WIDTH/2 -250/2, 595, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Quit')

    # main menu loop
    while True:

        # loops for every event
        for event in pygame.event.get():

            # if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mousebutton event handler
            if event.type == pygame.MOUSEBUTTONDOWN:

                # left click event
                if event.button == 1:

                    # if the user clicks the play button
                    if play_button.click():
                        game_choice_menu()

                    # if the user clicks the help button
                    if help_button.click():
                        pass

                    # if the user clicks the quit button
                    if quit_button.click():
                        pygame.quit()
                        sys.exit()

        # draw the background
        SCREEN.blit(BACKGROUND, (0,0))

        # draw the buttons
        play_button.draw()
        help_button.draw()
        quit_button.draw()

        # logo
        SCREEN.blit(LOGO_IMAGE, (WIDTH/2 - LOGO_IMAGE.get_width()/2, 10))

        # update the screen
        pygame.display.flip()

# function that initializes the game choice menu (case 2 and 3)
def game_choice_menu() -> None:

    global session_id, host_username

    # textbox initialization
    textbox = Textbox.Textbox(WIDTH/2 - 500/2, 325, 500, 55, FONT , 'Session ID')

    # button initialization
    join_button = Button.Button((WIDTH/2 - 250/2) + 125, 410, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Join')
    create_button = Button.Button(WIDTH/2 - 505/2, 410, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Create')
    back_button = Button.Button(WIDTH/2 - 250/2, 595, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Back')

    # game choice menu loop
    while True:

        # loops for every event
        for event in pygame.event.get():

            # if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mousebutton event handler
            if event.type == pygame.MOUSEBUTTONDOWN:

                # left click event
                if event.button == 1:

                    # if the user clicks the textbox
                    textbox.click()

                    # if the user clicks the join button
                    if join_button.click():
                        connection_result = connection.join_session(textbox.text)
                        if connection:
                            session_id = textbox.text
                            host_username = connection_result
                            lobby(0) # so i'm the guest
                        else:
                            textbox.text = 'Join error'

                    # if the user clicks the create button
                    if create_button.click():
                        if len(textbox.text) > 2 and connection.create_session(textbox.text):
                            session_id = textbox.text
                            lobby(1) # so i'm the host
                        else:
                            textbox.text = 'Creation error'

                    # if the user clicks the back button
                    if back_button.click():
                        main_menu()
            
            if event.type == pygame.KEYDOWN:
                textbox.write(event)

        # draw the background
        SCREEN.blit(BACKGROUND, (0,0))

        # draw the logo
        LOGO_SMALL = pygame.transform.scale(LOGO, (320, 240))
        SCREEN.blit(LOGO_SMALL, (WIDTH/2 - LOGO_SMALL.get_width()/2, 25))

        # draw the buttons & textbox
        join_button.draw()
        create_button.draw()
        back_button.draw()
        textbox.draw()

        # update the screen
        pygame.display.flip()

# function that asks for a specific string (case 0 and 1)
def string_request_screen(case : int) -> str:

    global server_ip, username

    """
        case 0: server_ip
        case 1: username
    """

    # textbox initialization
    if case == 0: textbox = Textbox.Textbox(WIDTH/2 - 500/2, 450, 500, 55, FONT , 'Server ip')
    if case == 1: textbox = Textbox.Textbox(WIDTH/2 - 500/2, 450, 500, 55, FONT , 'Username')

    # confirm button
    confirm_button = Button.Button(WIDTH/2 - 250/2, 520, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Confirm')

    # ip request screen loop
    while True:

        # loops for every event
        for event in pygame.event.get():

            # if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # back button or textbox click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    textbox.click()

                    if confirm_button.click():
                        try:
                            # server ip
                            if case == 0:
                                if connection.connect_to_server(textbox.text):
                                    server_ip = textbox.text
                                    return
                                else:
                                    textbox.text = 'ip error'
                                
                            # username
                            elif case == 1: 
                                if len(textbox.text) > 2 and connection.validate_username(textbox.text):
                                    username = textbox.text
                                    return
                                else:
                                    textbox.text = 'Name error'

                        except:
                            textbox.text = ''

            if event.type == pygame.KEYDOWN:
                textbox.write(event)

        # draw the background
        SCREEN.blit(BACKGROUND, (0,0))

        # draw the logo
        LOGO_SMALL = pygame.transform.scale(LOGO, (320, 240))
        SCREEN.blit(LOGO_SMALL, (WIDTH/2 - LOGO_SMALL.get_width()/2, 25))

        # draw the textbox & button
        textbox.draw()
        confirm_button.draw()

        # update the screen
        pygame.display.flip()

# listening for the guest
def listen_for_guest() -> None:

    global guest_username

    # saving the username
    guest_username = connection.listen_for_guest()

# listening for the start
def listen_for_start() -> None:

    global host_started

    # saving the username
    host_started = connection.listen_for_start()

# function that represents the lobby
def lobby (case : int) -> None:
        
        # listener thread
        my_listener = None

        # joined flag
        joined = False

        # my guest
        user_guest = None
        
        # guest and host variables
        host = username if case == 1 else host_username
        guest = username if case == 0 else None

        host_text = Button.Button(WIDTH/2 - 275, 330, button_width, button_height, BUTTON_BACKGROUND, FONT, host)
        guest_text = Button.Button(WIDTH/2 + 50, 330, button_width, button_height, BUTTON_BACKGROUND, FONT, guest)

        # host case
        if case == 1: 

            # create the start button
            start_button = Button.Button(WIDTH/2 - 250/2, 580, button_width, button_height, BUTTON_BACKGROUND, FONT, 'Start')

            # start thread to listen for guest
            my_listener = threading.Thread(target=listen_for_guest)
            my_listener.start()

        # guest case
        else:

            # start thread to listen for start
            my_listener = threading.Thread(target=listen_for_start)
            my_listener.start()
    
        # lobby loop
        while True:
    
            # loops for every event
            for event in pygame.event.get():

                if host_started:
                    game_loop(not case, guest, host)

                # if the guest joined
                if guest_username != '' and (not joined and case == 1):
                    joined = True
                    guest_text = Button.Button(WIDTH/2 + 50, 330, button_width, button_height, BUTTON_BACKGROUND, FONT, guest_username.split(":")[1].strip())
                    my_listener.join()

                # if the user closes the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                # mousebutton event handler
                if event.type == pygame.MOUSEBUTTONDOWN:
    
                    # left click event
                    if event.button == 1:
    
                        # if the host clicks the start button
                        if case == 1 and start_button.click():
                            if connection.start_game():
                                game_loop(not case, host, guest_username.split(":")[1].strip())
    
            # draw the background
            SCREEN.blit(BACKGROUND, (0,0))

            # draw the logo
            LOGO_SMALL = pygame.transform.scale(LOGO, (320, 240))
            SCREEN.blit(LOGO_SMALL, (WIDTH/2 - LOGO_SMALL.get_width()/2, 25))
    
            # draw the buttons
            start_button.draw() if case == 1 else None
            host_text.draw()
            guest_text.draw()
    
            # update the screen
            pygame.display.flip()

# listening for the move
def listen_for_move() -> None:

    global understood_move

    # saving the move
    understood_move = connection.listen_for_move()

# chess game loop
def game_loop(role : int, my_name : str, opponent_name : str) -> None:

    global understood_move

    # initialize engine class
    engine = Engine.Engine()

    # button initialization
    board = Chessboard.Chessboard(WIDTH/2 - (85*4), 20, 85, role)
    board.load_piece_images()

    # button names
    my_button = Button.Button(25, 570, button_width, button_height, BUTTON_BACKGROUND, FONT, my_name)
    opponent_button = Button.Button(25, 47, button_width, button_height, BUTTON_BACKGROUND, FONT, opponent_name)

    # selected piece
    selected_piece = None

    # my thread
    my_thread = None

    # my turn
    my_turn = False if role else True

    # guest case
    if role:
        my_thread = threading.Thread(target=listen_for_move).start()

    # main menu loop
    while True:

        # if i received something
        if understood_move != '':

            # perform the understood move
            engine.perform_move(understood_move.split(':')[1])
            
            # if alive join the thread
            my_thread.join() if my_thread else None

            # resets the global move var
            understood_move = ''

            # start of my turn
            my_turn = True

        # loops for every event
        for event in pygame.event.get():

            # if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # mouse position
                x, y = pygame.mouse.get_pos()

                if selected_piece is None:
                    # get the piece clicked
                    selected_piece = board.get_piece(x, y, board)
                    departure_square = board.square_to_uci(x, y, board)
                else:

                    if my_turn:

                        # get the destination square
                        destination_square = board.square_to_uci(x, y, board)

                        if engine.perform_move(departure_square + destination_square):

                            # send move to opponent
                            print(connection.send_message(f'MOVE:{"host" if not role else "guest"}:{departure_square + destination_square}'))

                            # my turn is over
                            my_turn = False

                            my_thread = threading.Thread(target=listen_for_move).start()

                    # reset selected piece and destination square
                    selected_piece = None
                    departure_square = None
                    destination_square = None

        # draw the background
        SCREEN.blit(BACKGROUND, (0,0))

        # draw the buttons
        board.draw()
        board.draw_pieces()
        my_button.draw()
        opponent_button.draw()

        # draw the selected piece
        if selected_piece is not None:
            i, square = selected_piece
            row, col = square // 8, square % 8
            if board.side:
                piece_x = board.x + (7 - col) * board.square_size
                piece_y = board.y + (7 - row) * board.square_size
            else:
                piece_x = board.x + col * board.square_size
                piece_y = board.y + row * board.square_size

            highlight_surface = pygame.Surface((board.square_size, board.square_size), pygame.SRCALPHA)
            highlight_surface.fill((255, 0, 0, 128))
            board.screen.blit(highlight_surface, (piece_x, piece_y))

        # update the screen
        pygame.display.flip()

# Entry point -------------------------------- #
if __name__ == '__main__':
    
    string_request_screen(0)
    string_request_screen(1)
    main_menu()