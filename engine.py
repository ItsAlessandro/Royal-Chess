# ---------------------------------------------------------------------- #
# Royal Chess - A Chess Game in Python
#
# Alessandro Duranti, 19 April 2024
# Latest revision: 19 April 2024
#
# Quick TODO guide for new users:
# 
# 1) Do this to run the networing search...
# 2) Do that to run the game...
# 3) Do this other thing to run the GUI...
# 
# Cedits, resources and people that helped me:
# - The Chess Programming Wiki - https://www.chessprogramming.org/
# - Chess Programming - https://www.youtube.com/@chessprogramming591
# 
# Enjoy Royal Chess!
# ---------------------------------------------------------------------- #

# Constant representation of the chess board, human readable way
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

# Bitboard util functions ------------------------------------------------- #

# Returns if a square is occupied or not
def get_bit(bitboard, square) -> bool:
    return bool(bitboard & (1 << square))

# Returns the updated bitboard with the square set to occupied
def set_bit(bitboard, square) -> int:
    return bitboard | (1 << square)

# Returns the updated bitboard with the square set to unoccupied (if possibile)
def clear_bit(bitboard, square) -> int:
    return bitboard ^ (1 << square) if get_bit(bitboard, square) else bitboard

# Prints the bitboard in a human readable way
def print_bitboard(bitboard) -> None:
    print()
    for rank in range(8):
        line = f"{8 - rank}  "
        for file in range(8):
            square = rank * 8 + file
            line += ("1" if get_bit(bitboard, square) else "0") + ' '
        print(line)
    print('\n   A B C D E F G H\n')

# ---------------------------------------------------------------------- #

# Entry point
bitboard = 0

bitboard = set_bit(bitboard, board_squares.index("a1"))
bitboard = set_bit(bitboard, board_squares.index("h8"))
bitboard = clear_bit(bitboard, board_squares.index("a1"))

print_bitboard(bitboard)