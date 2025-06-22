import pygame
import chess
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL cert warnings (for ngrok dev use only)
warnings.simplefilter("ignore", InsecureRequestWarning)

# Replace with your backend/ngrok URL
COLAB_URL = "PASTE_NGROK_URL_HERE/best_move"

# Initialize pygame
pygame.init()

# Constants
width, height = 750, 750
border = 25
FPS = 60
TILE_SIZE = (width - 2 * border) // 8

# Colors
x_color = (118, 150, 86)
y_color = (255, 255, 255)
bgcolor = (78, 78, 78)
selected_bg_color = (255, 255, 255)
selected_glow_color = (255, 0, 0, 100)
check_color = (255, 0, 0)
move_dot_color = (0, 0, 0)
capture_glow_color = (0, 255, 0, 100)

# Pygame setup
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")
pygame.font.init()
font = pygame.font.SysFont('Cambria', 40)

# Load piece images
piece_images = {}
piece_types = ['K', 'Q', 'R', 'B', 'N', 'P']
for piece in piece_types:
    piece_images[piece] = pygame.transform.scale(pygame.image.load(f'assets_v3/w{piece}.png'), (TILE_SIZE, TILE_SIZE))
    piece_images[piece.lower()] = pygame.transform.scale(pygame.image.load(f'assets_v3/b{piece}.png'), (TILE_SIZE, TILE_SIZE))

# Chess board initialization
board = chess.Board()
# custom_fen = "2r3k1/5ppp/1p6/8/3P4/1P3N2/5PPP/3R2K1 w - - 0 1"
# custom_fen = "8/8/8/2k5/3p4/3P4/6K1/8 w - - 0 1"
custom_fen = "8/8/8/8/6K1/8/6p1/6kq w - - 0 1"
board.set_fen(custom_fen)

# Game state
selected_square = None
move_from = None
game_over = False
winner = None

# -----------------------------------------------------------------------------------
# AI Move Fetch from Server

def get_best_move(board, depth=5):
    fen = board.fen()
    try:
        response = requests.post(
            COLAB_URL,
            json={"fen": fen, "depth": depth},
            timeout=10,
            verify=False
        )
        response.raise_for_status()
        best_move_str = response.json().get("best_move")
        if best_move_str:
            move = chess.Move.from_uci(best_move_str)
            print(f"[AI] Best move: {move}")
            return move
        print("[AI] No move returned.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[Error] Fetching best move: {e}")
        return None
# -----------------------------------------------------------------------------------

def draw_board():
    king_square = board.king(board.turn) if board.is_check() else None
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            color = (
                check_color if square == king_square else
                selected_bg_color if selected_square == (col, row) else
                x_color if (row + col) % 2 == 0 else y_color
            )
            pygame.draw.rect(window, color,
                             (border + col * TILE_SIZE, border + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if selected_square == (col, row):
                glow_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                glow_surface.fill(selected_glow_color)
                window.blit(glow_surface, (border + col * TILE_SIZE, border + row * TILE_SIZE))

def draw_pieces_from_board():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece.symbol()
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            window.blit(piece_images[symbol], (border + col * TILE_SIZE, border + row * TILE_SIZE))

def draw_move_dots():
    if move_from is not None:
        for move in board.legal_moves:
            if move.from_square == move_from:
                col = chess.square_file(move.to_square)
                row = 7 - chess.square_rank(move.to_square)
                center = (border + col * TILE_SIZE + TILE_SIZE // 2, border + row * TILE_SIZE + TILE_SIZE // 2)
                pygame.draw.circle(window, move_dot_color, center, TILE_SIZE // 6)
                if board.piece_at(move.to_square):
                    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    surface.fill(capture_glow_color)
                    window.blit(surface, (border + col * TILE_SIZE, border + row * TILE_SIZE))

def draw_game_over():
    if game_over:
        text = font.render(f"Game Over! {winner} Wins!", True, (255, 255, 255))
        restart = font.render("Press R to Restart", True, (255, 255, 255))
        box_w = max(text.get_width(), restart.get_width()) + 40
        box_h = text.get_height() + restart.get_height() + 30
        x = (width - box_w) // 2
        y = (height - box_h) // 2
        pygame.draw.rect(window, (0, 0, 0), (x, y, box_w, box_h))
        pygame.draw.rect(window, (255, 0, 0), (x, y, box_w, box_h), 5)
        window.blit(text, (x + 20, y + 10))
        window.blit(restart, (x + 20, y + text.get_height() + 15))

def draw():
    window.fill(bgcolor)
    draw_board()
    draw_pieces_from_board()
    draw_move_dots()
    draw_game_over()
    pygame.display.update()

def get_square_from_mouse(pos):
    x, y = pos
    col = (x - border) // TILE_SIZE
    row = (y - border) // TILE_SIZE
    return (col, row) if 0 <= col < 8 and 0 <= row < 8 else None

def reset_game():
    global board, selected_square, move_from, game_over, winner
    board = chess.Board()
    selected_square = None
    move_from = None
    game_over = False
    winner = None

def game():
    global selected_square, move_from, board, game_over, winner
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        if board.turn == chess.BLACK and not game_over:
            best_move = get_best_move(board, depth=5)
            if best_move:
                board.push(best_move)
                if board.is_checkmate():
                    game_over = True
                    winner = "Black"  # AI just played
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                clicked = get_square_from_mouse(event.pos)
                if clicked:
                    file, rank = clicked
                    square = chess.square(file, 7 - rank)
                    if move_from is None:
                        if board.piece_at(square) and board.piece_at(square).color == board.turn:
                            move_from = square
                            selected_square = clicked
                    else:
                        move_to = square
                        move = chess.Move(move_from, move_to)
                        if move in board.legal_moves:
                            board.push(move)
                            if board.is_checkmate():
                                game_over = True
                                winner = "White"
                        move_from = None
                        selected_square = None
        draw()
    pygame.quit()

if __name__ == "__main__":
    game()
