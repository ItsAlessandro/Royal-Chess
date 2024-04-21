# ---------------------------------------------------------------------- #
# Royal Chess - A Chess Game in Python
#
# Alessandro Duranti, 19 April 2024
# Latest revision: 19 April 2024
#
# Quick TODO guide for new users:
# 
# 1) Instructions for something...
# 2) Instructions for something...
# 3) Instructions for something...
# 
# Cedits, resources and people that helped me:
# - The Chess Programming Wiki - https://www.chessprogramming.org/
# - Chess Programming - https://www.youtube.com/@chessprogramming591
# 
# Enjoy Royal Chess!
# ---------------------------------------------------------------------- #

# Constants & Globals

# Representation of the chess board, human readable way
board_squares = [
  "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
  "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
  "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
  "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
  "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
  "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
  "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
  "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"
]

# Colors, sides to move
colors = [
    "white", "black"
]

# Banned files for pawn and knight attacks
not_a_file = 18374403900871474942 # pawns & knights
not_h_file = 9187201950435737471 # pawns & knights
not_ab_file = 18229723555195321596 # knight ext.
not_gh_file = 4557430888798830399 # knight ext.

# Possible attacks containers
pawn_attacks = [[0 for _ in range(64)] for _ in range(2)]
knight_attacks = [0 for _ in range(64)]
king_attacks = [0 for _ in range(64)]

# Bitboard utils ------------------------------------------------------- #

# Returns the index of a specific square
def square_enum(square : str) -> int:
    return board_squares.index(square)

# Returns the index of black or white
def color_enum(color : str) -> int:
    return colors.index(color)

# Returns if a square is occupied or not
def get_bit(bitboard : int, square : int) -> bool:
    return bool(bitboard & (1 << square))

# Updates a bitboard specific square to occupied
def set_bit(bitboard : int, square : int ) -> int:
    return bitboard | (1 << square)

# Updates a bitboard specific square to unoccupied
def clear_bit(bitboard : int, square : int) -> None:
    bitboard ^ (1 << square) if get_bit(bitboard, square) else bitboard

# Prints the passed bitboard
def print_bitboard(bitboard : int) -> None:
    
    # container for bitboard lines
    line = ''

    # initial styling newline
    print()

    for rank in range(8):
        line = f"{8 - rank}  "
        for file in range(8):
            square = rank * 8 + file
            line += ("1" if get_bit(bitboard, square) else "0") + ' '
        print(line)

    print('\n   A B C D E F G H\n')

    print(f"Bitboard: {bitboard}\n")

# ---------------------------------------------------------------------- #

# Attack generation ---------------------------------------------------- #

# Returns the possible attacks for a pawn of a certain side in a certain position
def mask_pawn_attacks(side : int, square : int) -> int:

    # result attacks bitboard
    attacks = 0

    # test container
    bitboard = 0

    # inserting the piece in the bitboard
    bitboard = set_bit(bitboard, square)

    # white pawns
    if not side:
        if bitboard >> 7 & not_a_file: attacks |= (bitboard >> 7)
        if bitboard >> 9 & not_h_file: attacks |= (bitboard >> 9)
    
    # black pawns
    else:
        if bitboard << 7 & not_h_file: attacks |= (bitboard << 7)
        if bitboard << 9 & not_a_file: attacks |= (bitboard << 9)

    return attacks

# Returns the possible attacks for a knight of a certain side in a certain position
def mask_knight_attacks(square : int) -> int:

    # result attacks bitboard
    attacks = 0

    # test container
    bitboard = 0

    # inserting the piece in the bitboard
    bitboard = set_bit(bitboard, square)

    if bitboard >> 6 & not_ab_file: attacks |= (bitboard >> 6)
    if bitboard << 10 & not_ab_file: attacks |= (bitboard << 10)
    if bitboard >> 15 & not_a_file: attacks |= (bitboard >> 15)
    if bitboard << 17 & not_a_file: attacks |= (bitboard << 17)
    

    if bitboard << 6 & not_gh_file: attacks |= (bitboard << 6)
    if bitboard >> 10 & not_gh_file: attacks |= (bitboard >> 10)
    if bitboard << 15 & not_h_file: attacks |= (bitboard << 15)
    if bitboard >> 17 & not_h_file: attacks |= (bitboard >> 17)
    
    return attacks

# Returns the possible attacks for a king in a certain position
def mask_king_attacks(square : int) -> int:
    
    # result attacks bitboard
    attacks = 0

    # test container
    bitboard = 0

    # inserting the piece in the bitboard
    bitboard = set_bit(bitboard, square)

    # TODO : possible bug here
    if bitboard >> 1 & not_h_file: 
        attacks |= (bitboard >> 1)
        attacks |= (bitboard >> 9)
        attacks |= (bitboard << 7)

    if bitboard << 1 & not_a_file:
        attacks |= (bitboard << 1)
        attacks |= (bitboard << 9)
        attacks |= (bitboard >> 7)
        
    attacks |= (bitboard >> 8)
    attacks |= (bitboard << 8)

    return attacks

# Returns the possible attacks for a bishop in a certain position
def mask_bishop_attacks(square : int) -> int:
    
    # result attacks bitboard
    attacks = 0

    # init ranks & files
    r = f = 0

    # init target rank & files
    tr = square // 8
    tf = square % 8

    for r, f in zip(range(tr + 1, 7), range(tf + 1, 7)): attacks |= (1 << (r * 8 + f))
    for r, f in zip(range(tr - 1, 0, -1), range(tf + 1, 7)): attacks |= (1 << (r * 8 + f))
    for r, f in zip(range(tr + 1, 7), range(tf - 1, 0, -1)): attacks |= (1 << (r * 8 + f))
    for r, f in zip(range(tr - 1, 0, -1), range(tf - 1, 0, -1)): attacks |= (1 << (r * 8 + f))

    return attacks

# Returns the possible attacks for a rook in a certain position
def mask_rook_attacks(square: int) -> int:
    # result attacks bitboard
    attacks = 0

    # init target rank & files
    tr = square // 8
    tf = square % 8

    # mask relevant rook occupancy bits
    for r in range(tr + 1, 7): attacks |= (1 << (r * 8 + tf))
    for r in range(tr - 1, 0, -1): attacks |= (1 << (r * 8 + tf))
    for f in range(tf + 1, 7): attacks |= (1 << (tr * 8 + f))
    for f in range(tf - 1, 0, -1): attacks |= (1 << (tr * 8 + f))

    # return attack map
    return attacks

# For every square on the board, it calculates the possible (w & b) pawn attacks
def init_leaper_attacks() -> None:

    # pawns
    for i in range(64):
        pawn_attacks[color_enum('white')][i] = mask_pawn_attacks(color_enum('white'), i)
        pawn_attacks[color_enum('black')][i] = mask_pawn_attacks(color_enum('black'), i)

    # knights
    for i in range(64):
        knight_attacks[i] = mask_knight_attacks(i)

    # kings
    for i in range(64):
        king_attacks[i] = mask_king_attacks(i)

# ---------------------------------------------------------------------- #

# Testing

init_leaper_attacks()

for i in range(64):
    print_bitboard(mask_rook_attacks(i))