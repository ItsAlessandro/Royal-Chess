import pygame

# Importing bitboards and occupancies
from models.engine.engine import bitboards
from models.engine.engine import occupancies

class Chessboard:
    def __init__(self, x, y, square_size, side):
        self.x = x
        self.y = y
        self.square_size = square_size
        self.board_size = 8 * square_size
        self.screen = pygame.display.get_surface()
        self.rect = pygame.Rect(x, y, self.board_size, self.board_size)
        self.colors = [(251, 252, 228, 243), (104, 72, 148, 235)]
        self.side = side # 0 for white, 1 for black
        self.pieces = {} # loaded images as pieces

    def load_piece_images(self):
        piece_types = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
        for color in ['white', 'black']:
            for piece in piece_types:
                image = pygame.image.load(f'././resources/images/pieces/{color}-{piece}.png')
                image = pygame.transform.scale(image, (self.square_size, self.square_size))
                self.pieces[(color, piece)] = image

    def draw(self):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                square_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                square_surface.fill(color)
                self.screen.blit(square_surface, (self.x + col * self.square_size, self.y + row * self.square_size))
        

    def draw_pieces(self) -> None:
        piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        
        # every piece type
        for i in range(12):

            # black or white side
            side = 0 if i < 6 else 1
                
            # for every square
            for square in range(64):
                if (bitboards[i] & occupancies[side]) & (1 << square):
                    row, col = square // 8, square % 8
                    if self.side:
                        x = self.x + (7 - col) * self.square_size
                        y = self.y + (7 - row) * self.square_size
                    else:
                        x = self.x + col * self.square_size
                        y = self.y + row * self.square_size
                    self.screen.blit(self.pieces[('white' if not side else 'black', piece_types[i % 6])], (x, y))

    def get_piece(self, x, y, board) -> tuple:

        for i in range(12):
            side = 0 if i < 6 else 1
            if side != self.side: # only pieces of my side
                continue
        
            for square in range(64):
                if (bitboards[i] & occupancies[side]) & (1 << square):
                    row, col = square // 8, square % 8
                    if self.side:
                        piece_x = board.x + (7 - col) * board.square_size
                        piece_y = board.y + (7 - row) * board.square_size
                    else:
                        piece_x = board.x + col * board.square_size
                        piece_y = board.y + row * board.square_size
                    if piece_x <= x < piece_x + board.square_size and piece_y <= y < piece_y + board.square_size:
                        # select the piece
                        selected_piece = (i, square)
                        return selected_piece
    
    def square_to_uci(self, x, y, board):
        # Calculate the column and row in the chessboard grid

        if self.side == 0:
            col = (x - board.x) // board.square_size
            row = (y - board.y) // board.square_size
        else:
            col = 7 - (x - board.x) // board.square_size
            row = 7 - (y - board.y) // board.square_size

        # Map the column and row to the corresponding file and rank
        file = chr(ord('a') + int(col))
        rank = 8 - row

        # Return the UCI notation of the square
        return f'{file}{rank}'