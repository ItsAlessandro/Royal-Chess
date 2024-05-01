# ---------------------------------------------------------------------- #
# Royal Chess - A Chess Game in Python
#
# Alessandro Duranti, 19 April 2024
# Latest revision: 29 April 2024
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

# TODO : for the refactored version of the engine
# TODO : fix magic numbers generation (optional)
# TODO : macros & enums functions on top (essential)

# Imports 

from constants import ROOK_MAGICS, BISHOP_MAGICS

# Constants & Globals

# FEN strings
empty_board = "8/8/8/8/8/8/8/8 w - - "
start_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
tricky_position = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQq - 0 1 "
killer_position = "rnbqkb1r/pp1p1pPp/8/2p1pP2/1P1P4/3P3P/P1P1P3/RNBQKBNR b KQkq h1 0 1"
cmk_position = "r2q1rk1/ppp2ppp/2n1bn2/2b1p3/3pP3/3P1NPP/PPP1NPB1/R1BQ1RK1 b q - 0 9 "

# Representation of the chess board, human readable way
board_squares = [
  "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
  "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
  "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
  "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
  "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
  "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
  "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
  "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "no_sq"
]

# Colors, sides to move
colors = [
    "white", "black", "both"
]

# Slider pieces flags
sliders = [
    'rook', 'bishop'
]

# Castling bits
castle_flags = {
    'wk': 1, # 0001
    'wq': 2, # 0010
    'bk': 4, # 0100
    'bq': 8  # 1000
}

# Encode pieces
pieces = [
    'P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'
]

# ASCII pieces
ascii_pieces = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

# Define bitboards
bitboards = [0 for _ in range(12)]

# Define occupancies
occupancies = [0 for _ in range(3)] # white, black, both

# Python way TODO : use a class to fix this mess (in python is not possible to modify in functions primitive dt)
current_props = [0, board_squares.index('no_sq'), 0] # side, enpassant, castle

"""
# ORIGINAL WAY: ------------------------------------------------------- #

# Side to move
side = 0

# Enpassant square
enpassant = board_squares.index('no_sq')

# Castling rights
castle = 0

# ---------------------------------------------------------------------- #
"""

# Banned files for pawn and knight attacks
not_a_file = 18374403900871474942 # pawns & knights
not_h_file = 9187201950435737471 # pawns & knights
not_ab_file = 18229723555195321596 # knight ext.
not_gh_file = 4557430888798830399 # knight ext.

# relevant occupancy bit count
bishop_relevant_bits = [
    6, 5, 5, 5, 5, 5, 5, 6, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    5, 5, 7, 7, 7, 7, 5, 5, 
    5, 5, 7, 9, 9, 7, 5, 5, 
    5, 5, 7, 9, 9, 7, 5, 5, 
    5, 5, 7, 7, 7, 7, 5, 5, 
    5, 5, 5, 5, 5, 5, 5, 5, 
    6, 5, 5, 5, 5, 5, 5, 6
]
rook_relevant_bits = [
    12, 11, 11, 11, 11, 11, 11, 12, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    11, 10, 10, 10, 10, 10, 10, 11, 
    12, 11, 11, 11, 11, 11, 11, 12,
]

# Possible attacks containers
pawn_attacks = [[0 for _ in range(64)] for _ in range(2)]
knight_attacks = [0 for _ in range(64)]
king_attacks = [0 for _ in range(64)]

# Bishop attack masks
bishop_masks = [0 for _ in range(64)]

# Rooke attack masks
rook_masks = [0 for _ in range(64)]

# Bishops attack table
bishop_attacks = [[0 for _ in range(512)] for _ in range(64)]

# Rook attack table
rook_attacks = [[0 for _ in range(4096)] for _ in range(64)]

# Bitboard utils ------------------------------------------------------- #

# Returns the index of a specific piece
def piece_enum(piece : str) -> int:
    return pieces.index(piece)

# Returns the index of a specific square
def square_enum(square : str) -> int:
    return board_squares.index(square)

# Returns the index of black or white
def color_enum(color : str) -> int:
    return colors.index(color)

# Returns the index of a specific piece (rook or bishop) # TODO NAMING PROBLEM HERE
def slider_enum(piece : str) -> int:
    return sliders.index(piece)

# Returns if a square is occupied or not
def get_bit(bitboard : int, square : int) -> bool:
    return bool(bitboard & (1 << square))

# Updates a bitboard specific square to occupied
def set_bit(bitboard : int, square : int ) -> int:
    return bitboard | (1 << square)

# Updates a bitboard specific square to unoccupied
def clear_bit(bitboard : int, square : int) -> None:
    return bitboard ^ (1 << square) if get_bit(bitboard, square) else bitboard

# Count bits in a bitboard
def count_bits(bitboard : int) -> int:

    # counter
    count = 0

    # reset least significant bit (while exists)
    while bitboard:
        bitboard &= bitboard - 1
        count += 1

    # returning the number of bits
    return count

# Returns the least significant 1 bit index
def get_ls1b_index(bitboard : int) -> int:
    
    # make sure bitboard is not 0
    if bitboard:

        # count trailing bits before LS1B
        return count_bits((bitboard & -bitboard) - 1)
    
    else:

        # return illegal index
        return -1

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

def print_board() -> None:
    
    # container for bitboard lines
    line = ''

    # initial styling newline
    print()

    for rank in range(8):
        line = f"{8 - rank}  "
        for file in range(8):
            square = rank * 8 + file
            piece = ' '
            for i in range(12):
                if get_bit(bitboards[i], square):
                    piece = ascii_pieces[pieces[i]]
                    break

            line += (piece if piece != ' ' else '.') + ' '
        print(line)

    print('\n   A B C D E F G H\n')

    # side to move
    print(f"Side to move: {colors[color_enum('black')] if current_props[0] else colors[color_enum('white')]}\n")

    # enpassant TODO : fix this
    print(f"Enpassant: {board_squares[square_enum(current_props[1])] if current_props[1] != square_enum('no_sq') else 'no'}\n")

    # castling rights
    print(f'Castling: {"K" if current_props[2] & castle_flags["wk"] else "-"}{"Q" if current_props[2] & castle_flags["wq"] else "-"}{"k" if current_props[2] & castle_flags["bk"] else "-"}{"q" if current_props[2] & castle_flags["bq"] else "-"}\n')

# parse FEN strings
def parse_fen(fen : str) -> None:

    # reset boards
    for i in range(12): bitboards[i] = 0
    for i in range(3): occupancies[i] = 0

    # reset state
    for i in range(3): 
        if i == 1: current_props[i] = 'no_sq'
        else: current_props[i] = 0

    # index utilized to iterate over the FEN string
    fen_index = 0

    # loop over FEN string

    rank = 0
    while rank < 8:

        file = 0
        while file < 8:

            square = rank * 8 + file
            piece = fen[fen_index]

            if piece.isnumeric() or piece == '/' or piece == ' ':
                if piece.isnumeric():
                    file += (int(piece) - 1)

                elif piece == '/':
                    fen_index += 1
                    rank += 1
                    break

                else:
                    rank = 8
                    break

            else:
                piece_index = piece_enum(piece)
                bitboards[piece_index] = set_bit(bitboards[piece_index], square)

            file += 1
            fen_index += 1
    
    # jumping over the space
    fen_index += 1

    # side to move
    current_props[0] = color_enum('white') if fen[fen_index] == 'w' else color_enum('black')

    # jumping over the space
    fen_index += 2

    # castling parse
    while fen[fen_index] != ' ':
        if fen[fen_index] == 'K': current_props[2] |= castle_flags['wk']
        if fen[fen_index] == 'Q': current_props[2] |= castle_flags['wq']
        if fen[fen_index] == 'k': current_props[2] |= castle_flags['bk']
        if fen[fen_index] == 'q': current_props[2] |= castle_flags['bq']
        if fen[fen_index] == '-': break

        fen_index += 1

    # jumping over the spaces
    while fen[fen_index] == ' ':
        fen_index += 1

    # enpassant square
    if fen[fen_index] != '-':
        current_props[1] = f'{fen[fen_index]}{fen[fen_index + 1]}'
    else:
        current_props[1] = square_enum('no_sq')

    # loop over white pieces
    for i in range(6):
        occupancies[color_enum('white')] |= bitboards[i]
    
    # loop over black pieces
    for i in range(6, 12):
        occupancies[color_enum('black')] |= bitboards[i]

    # loop over both colors
    occupancies[color_enum('both')] = occupancies[color_enum('white')] | occupancies[color_enum('black')]
    

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

# Bishop fly attacks
def bishop_fly_attacks(square: int, block : int) -> int:
    # result attacks bitboard
    attacks = 0

    # init ranks & files
    r = f = 0

    # init target rank & files
    tr = square // 8
    tf = square % 8

    # generate bishop attacks
    for r, f in zip(range(tr + 1, 8), range(tf + 1, 8)):
        attacks |= (1 << (r * 8 + f))
        if (1 << (r * 8 + f)) & block:
            break

    for r, f in zip(range(tr - 1, -1, -1), range(tf + 1, 8)):
        attacks |= (1 << (r * 8 + f))
        if (1 << (r * 8 + f)) & block:
            break

    for r, f in zip(range(tr + 1, 8), range(tf - 1, -1, -1)):
        attacks |= (1 << (r * 8 + f))
        if (1 << (r * 8 + f)) & block:
            break

    for r, f in zip(range(tr - 1, -1, -1), range(tf - 1, -1, -1)):
        attacks |= (1 << (r * 8 + f))
        if (1 << (r * 8 + f)) & block:
            break

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

# Rook fly attacks
def rook_fly_attacks(square: int, block : int) -> int:
    # result attacks bitboard
    attacks = 0

    # init ranks & files
    r = f = 0

    # init target rank & files
    tr = square // 8
    tf = square % 8

    for r in range(tr + 1, 8):
        attacks |= (1 << (r * 8 + tf))
        if (1 << (r * 8 + tf)) & block:
            break

    for r in range(tr - 1, -1, -1):
        attacks |= (1 << (r * 8 + tf))
        if (1 << (r * 8 + tf)) & block:
            break

    for f in range(tf + 1, 8):
        attacks |= (1 << (tr * 8 + f))
        if (1 << (tr * 8 + f)) & block:
            break

    for f in range(tf - 1, -1, -1):
        attacks |= (1 << (tr * 8 + f))
        if (1 << (tr * 8 + f)) & block:
            break

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

# set occupancies
def set_occupancy(index : int, bits_in_mask : int, attack_mask : int) -> int:

    # occupancy map
    occupancy = 0

    # loop over range of bits in mask
    for count in range(bits_in_mask):

        # get LS1B index
        square = get_ls1b_index(attack_mask)

        # pop LS1B
        attack_mask = clear_bit(attack_mask, square)
        
        # if occupancy bit is set
        if index & (1 << count):

            # set bit in occupancy map
            occupancy |= (1 << square)

    # return occupancy map
    return occupancy

# ---------------------------------------------------------------------- #

# Random number generator ---------------------------------------------- #

# pseudo number state
random_state = 1804289383

# generate 32 bits random number
def get_random_U32_number() -> int:

    # global declaration
    global random_state

    # get current state
    number = random_state

    # XOR shift algorithm
    number ^= (number << 13) & 0xFFFFFFFF
    number ^= number >> 17
    number ^= (number << 5) & 0xFFFFFFFF

    # update state
    random_state = number

    # return random number
    return number

# generate 64 bits random number
def get_random_U64_number() -> int:
    
    # define 4 random numbers
    a = b = c = d = 0

    # init random numbers
    a = get_random_U32_number() & 0xFFFF
    b = get_random_U32_number() & 0xFFFF
    c = get_random_U32_number() & 0xFFFF
    d = get_random_U32_number() & 0xFFFF
    
    # return 64 bits random number
    return a | (b << 16) | (c << 32) | (d << 48)

# generate magic number candidates
def generate_magic_number() -> int:
    return get_random_U64_number() & get_random_U64_number() & get_random_U64_number()

# ---------------------------------------------------------------------- #

# Magic bitboards ------------------------------------------------------ #

# find appropriate magic number
def find_magic_number(square : int, relevant_bits : int, bishop : int) -> int:

    # init occupancies
    occupancies = [0 for _ in range(4096)]

    # init attacks
    attacks = [0 for _ in range(4096)]

    # init used attacks
    used_attacks = [0 for _ in range(4096)]

    # init attack mask for current piece
    attack_mask = mask_bishop_attacks(square) if bishop else mask_rook_attacks(square)

    # init occupancy indices
    occupancy_indices = 1 << relevant_bits

    # loop over occupancy indices
    for index in range(occupancy_indices):

        # init occupancies
        occupancies[index] = set_occupancy(index, relevant_bits, attack_mask)

        # init attacks
        attacks[index] = bishop_fly_attacks(square, occupancies[index]) if bishop else rook_fly_attacks(square, occupancies[index])

    # testing
    for random_count in range(10000):

        # generate magic candidate
        magic_number = generate_magic_number()

        # skip if magic number is not valid
        if count_bits((attack_mask * magic_number) & 0xFF00000000000000) < 6: continue

        used_attacks = [0] * len(used_attacks)

        # init index & fail flag
        fail = 0

        # test magic index loop
        for index in range(occupancy_indices):

            # fail flag check
            if fail: break

            # init magic index
            magic_index = ((occupancies[index] * magic_number) & 0xffffffffffffffff) >> (64 - relevant_bits)

            # if magic index works
            if used_attacks[magic_index] == 0:

                # init used attacks
                used_attacks[magic_index] = attacks[index]

            elif used_attacks[magic_index] != attacks[index]:
                
                # magic index does not work
                fail = 1
        
        # if magic number is valid returns it
        if not fail:
            return magic_number

    return 0

# init magic numbers
def init_magic_numbers() -> None:

    # loop over all squares
    for square in range(64):

        # init rook magic numbers
        result = find_magic_number(square, bishop_relevant_bits[square], slider_enum('bishop'))

        if result != 0:
            print(f'0x{format(result, "016X")}')



# init slider pieces attack tables
def init_sliders_attacks (bishop : int) -> None:

    # loop over all squares
    for square in range(64):
        
        # init bishop and rook masks
        bishop_masks[square] = mask_bishop_attacks(square)
        rook_masks[square] = mask_rook_attacks(square)

        # init current mask
        attack_mask = bishop_masks[square] if bishop else rook_masks[square]

        # init relevant bits
        relevant_bits_count = count_bits(attack_mask)

        # init occupancy indices
        occupancy_indices = 1 << relevant_bits_count

        # loop over occupancy indices
        for index in range(occupancy_indices):

            # bishop
            if bishop:

                # init current occupancy variation
                occupancy = set_occupancy(index, relevant_bits_count, attack_mask)

                # init magic index
                magic_index = ((occupancy * BISHOP_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF) >> (64 - bishop_relevant_bits[square])

                # init bishop attacks
                bishop_attacks[square][magic_index] = bishop_fly_attacks(square, occupancy)

            # rook
            else:
                
                # init current occupancy variation
                occupancy = set_occupancy(index, relevant_bits_count, attack_mask)

                # init magic index
                magic_index = ((occupancy * ROOK_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF) >> (64 - rook_relevant_bits[square])

                # init rook attacks
                rook_attacks[square][magic_index] = rook_fly_attacks(square, occupancy)

# get bishop attacks
def get_bishop_attacks(square : int, occupancy : int) -> int:

    # get bishop attacks assuming current board occupancy
    occupancy &= bishop_masks[square]
    occupancy = (occupancy * BISHOP_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF
    occupancy >>= (64 - bishop_relevant_bits[square]) 

    return bishop_attacks[square][occupancy & len(bishop_attacks[square]) - 1]

# get rook attacks
def get_rook_attacks(square : int, occupancy : int) -> int:

    # get rook attacks assuming current board occupancy
    occupancy &= rook_masks[square]
    occupancy = (occupancy * ROOK_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF
    occupancy >>= 64 - rook_relevant_bits[square]

    return rook_attacks[square][occupancy & len(rook_attacks[square]) - 1]

# get queen attacks
def get_queen_attacks(square : int, occupancy : int) -> int:

    # init result attacks
    queen_attacks = 0

    # init bishop occupancies
    bishop_occupancy = occupancy
    # print_bitboard(f'Initial occupancy: {occupancy}')

    # init rook occupancies
    rook_occupancy = occupancy

    # get bishop attacks assuming current board occupancy
    bishop_occupancy &= bishop_masks[square]
    bishop_occupancy = (bishop_occupancy * BISHOP_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF
    bishop_occupancy >>= 64 - bishop_relevant_bits[square]

    # get bishop attacks
    queen_attacks = bishop_attacks[square][bishop_occupancy]

    # get rook attacks assuming current board occupancy
    rook_occupancy &= rook_masks[square]
    rook_occupancy = (rook_occupancy * ROOK_MAGICS[square]) & 0xFFFFFFFFFFFFFFFF
    rook_occupancy >>= 64 - rook_relevant_bits[square]

    # get rook attacks
    queen_attacks |= rook_attacks[square][rook_occupancy]

    # return queen attacks
    return queen_attacks

# is square attacked by the opposite color of "side"
def is_square_attacked(square : int, side : int) -> bool:

    if side == color_enum('white') and (pawn_attacks[color_enum('black')][square] & bitboards[piece_enum('P')]): return True

    if side == color_enum('black') and (pawn_attacks[color_enum('white')][square] & bitboards[piece_enum('p')]): return True

        # attacked by knights
    if knight_attacks[square] & (bitboards[piece_enum('N')] if side == color_enum('white') else bitboards[piece_enum('n')]): return True

    # attacked by bishops
    if get_bishop_attacks(square, occupancies[color_enum('both')]) & (bitboards[piece_enum('B')] if side == color_enum('white') else bitboards[piece_enum('b')]): return True

    # attacked by rooks
    if get_rook_attacks(square, occupancies[color_enum('both')]) & (bitboards[piece_enum('R')] if side == color_enum('white') else bitboards[piece_enum('r')]): return True

    # attacked by queens
    if get_queen_attacks(square, occupancies[color_enum('both')]) & (bitboards[piece_enum('Q')] if side == color_enum('white') else bitboards[piece_enum('q')]): return True

    # attacked by kings
    if king_attacks[square] & (bitboards[piece_enum('K')] if side == color_enum('white') else bitboards[piece_enum('k')]): return True

    # by default return false
    return False

# print attacked squares
def print_attacked_squares(side):

    # container for bitboard lines
    line = ''

    # initial styling newline
    print()

    for rank in range(8):
        line = f"{8 - rank}  "
        for file in range(8):
            square = rank * 8 + file
            line += f"{1 if is_square_attacked(square, side) else 0} "
        
        print(line)

    print('\n   A B C D E F G H\n')

# ---------------------------------------------------------------------- #

# Leaper attacks initializer
init_leaper_attacks()

# Attack initializers
init_sliders_attacks(slider_enum('bishop'))
init_sliders_attacks(slider_enum('rook'))

parse_fen(tricky_position)
print_board()

# print who attacks
print_attacked_squares(color_enum('white'))