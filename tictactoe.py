import tkinter
from easyAI import TwoPlayerGame, AI_Player, Human_Player
from easyAI import Negamax

# Initial Variables
playerX = "X"
playerO = "O"
curr_player = playerX
color_blue = '#4584b6'
color_yellow = '#ffde57'
color_grey = '#343434'
play_mode = "local"  # Default play mode

# Tkinter window setup
window = tkinter.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)

# Initialize board as 3x3 grid of None
board = [[None, None, None] for _ in range(3)]

# Define TicTacToe game class for AI
class TicTacToe(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        # Translate the 2D board into a 1D array
        self.board = [0 if board[row][col]["text"] == "" else
                      (1 if board[row][col]["text"] == playerX else 2)
                      for row in range(3) for col in range(3)]
        self.current_player = 1  # player 1 (AI) starts when AI plays

    def possible_moves(self):
        # List all the empty squares on the board
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, move):
        self.board[move] = self.current_player

    def unmake_move(self, move):
        self.board[move] = 0

    def is_over(self):
        # Check for a winner or if the board is full
        return self.check_winner() or all(self.board)

    def check_winner(self):
        # Winning combinations for the Tic Tac Toe board
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != 0:
                return self.board[combo[0]]
        return 0

    def scoring(self):
        return 100 if self.check_winner() == self.current_player else 0

# Menu Screen with Theme
def menu_screen():
    for widget in window.winfo_children():
        widget.destroy()

    menu_frame = tkinter.Frame(window, background=color_grey)
    menu_label = tkinter.Label(menu_frame, text="Choose Game Mode", font=('Consolas', 20),
                               foreground="white", background=color_grey)
    menu_label.pack(pady=(20, 10))

    local_button = tkinter.Button(menu_frame, text="Play Locally", font=("Consolas", 20),
                                  background=color_grey, foreground="white",
                                  command=lambda: start_game("local"))
    local_button.pack(pady=5)

    computer_button = tkinter.Button(menu_frame, text="Play with Computer", font=("Consolas", 20),
                                     background=color_grey, foreground="white",
                                     command=choose_letter_screen)
    computer_button.pack(pady=5)

    menu_frame.pack()

# Choose Letter Screen for Playing with Computer
def choose_letter_screen():
    for widget in window.winfo_children():
        widget.destroy()

    choose_frame = tkinter.Frame(window, background=color_grey)
    choose_label = tkinter.Label(choose_frame, text="Choose your letter", font=('Consolas', 20),
                                 foreground="white", background=color_grey)
    choose_label.pack(pady=(20, 10))

    x_button = tkinter.Button(choose_frame, text="X", font=("Consolas", 20),
                              background=color_grey, foreground=color_blue,
                              command=lambda: start_game("computer", "X"))
    x_button.pack(side="left", padx=20)

    o_button = tkinter.Button(choose_frame, text="O", font=("Consolas", 20),
                              background=color_grey, foreground=color_yellow,
                              command=lambda: start_game("computer", "O"))
    o_button.pack(side="right", padx=20)

    choose_frame.pack()

# Start Game
def start_game(mode, player_letter="X"):
    global play_mode, curr_player, playerX, playerO, board

    play_mode = mode
    playerX = player_letter
    playerO = "O" if player_letter == "X" else "X"
    curr_player = playerX

    # Reset board
    board = [[None, None, None] for _ in range(3)]
    game_screen()

def game_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame = tkinter.Frame(window)
    label = tkinter.Label(frame, text=curr_player + "'s turn", font=('Consolas', 20),
                          background=color_grey, foreground='white')
    label.grid(row=0, column=0, columnspan=3, sticky="we")

    for row in range(3):
        for column in range(3):
            board[row][column] = tkinter.Button(frame, text="", font=("Consolas", 50, "bold"),
                                                background=color_grey, foreground=color_blue, width=4, height=1,
                                                command=lambda row=row, column=column: player_move(row, column, label))
            board[row][column].grid(row=row + 1, column=column)

    button_main_menu = tkinter.Button(frame, text="Main Menu", font=("Consolas", 20), background=color_grey, foreground="white",
                                      command=menu_screen)
    button_main_menu.grid(row=4, column=0, columnspan=1, sticky="we")

    button_restart = tkinter.Button(frame, text="Restart Game", font=("Consolas", 20), background=color_grey, foreground="white",
                                    command=lambda: start_game(play_mode, playerX))
    button_restart.grid(row=4, column=1, columnspan=2, sticky="we")

    frame.pack()

def player_move(row, column, label):
    global curr_player

    if board[row][column]["text"] == "":
        board[row][column]["text"] = curr_player

        if check_winner():
            label.config(text=f"{curr_player} wins!")
            disable_board()
        elif is_tie():
            label.config(text="It's a tie!")
            disable_board()
        else:
            curr_player = playerO if curr_player == playerX else playerX
            label.config(text=f"{curr_player}'s turn")

            if play_mode == "computer" and curr_player == playerO:
                disable_board()
                window.after(500, lambda: computer_move(label))

def disable_board():
    for row in range(3):
        for col in range(3):
            board[row][col].config(state="disabled")

def enable_board():
    for row in range(3):
        for col in range(3):
            board[row][col].config(state="normal")

# Use AI with Negamax for the computer's turn
def computer_move(label):
    global curr_player
    ai_algo = Negamax(9)
    game = TicTacToe([AI_Player(ai_algo), Human_Player()])

    ai_move = game.players[0].ask_move(game)
    row, col = divmod(ai_move, 3)

    board[row][col]["text"] = curr_player

    if check_winner():
        label.config(text=f"{curr_player} wins!")
        disable_board()
    elif is_tie():
        label.config(text="It's a tie!")
        disable_board()
    else:
        curr_player = playerX
        label.config(text=f"{curr_player}'s turn")
        enable_board()

def is_tie():
    for row in range(3):
        for column in range(3):
            if board[row][column]["text"] == "":
                return False
    return True

def check_winner():
    for i in range(3):
        if board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"] != "":
            return True
        if board[0][i]["text"] == board[1][i]["text"] == board[2][i]["text"] != "":
            return True
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        return True
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        return True
    return False

# Start with the menu screen
menu_screen()
window.mainloop()
