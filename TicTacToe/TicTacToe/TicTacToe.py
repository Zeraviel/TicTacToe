import tkinter as tk
from tkinter import ttk, messagebox
import random

def check_win(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    # Check if the board is full
    return all(cell != " " for row in board for cell in row)

def on_click(row, col):
    global current_player

    if board[row][col] == " " and not game_over:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state=tk.DISABLED)
        
        if check_win(board, current_player):
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_board()
        elif is_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_board()
        else:
            current_player = "O" if current_player == "X" else "X"
            if current_player == ai_player:
                make_ai_move()

def make_ai_move():
    global current_player

    if ai_player == "X":
        if ai_difficulty == "Easy":
            _, best_move = easy_ai(board, ai_player)
        elif ai_difficulty == "Normal":
            _, best_move = normal_ai(board, ai_player)
        else:  # Default to Minimax if AI difficulty is not recognized
            _, best_move = minimax(board, ai_player)
    else:
        if ai_difficulty == "Easy":
            _, best_move = easy_ai(board, ai_player)
        elif ai_difficulty == "Normal":
            _, best_move = normal_ai(board, ai_player)
        else:  # Default to Minimax if AI difficulty is not recognized
            _, best_move = minimax(board, ai_player)

    row, col = best_move
    on_click(row, col)

def reset_board():
    global board, current_player, game_over
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = player_choice.get()
    game_over = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state=tk.NORMAL)

def minimax(board, player):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]

    if check_win(board, ai_player):
        return 1, None
    elif check_win(board, player_choice.get()):
        return -1, None
    elif not empty_cells:
        return 0, None

    moves = []
    for row, col in empty_cells:
        board[row][col] = player
        if player == ai_player:
            score, _ = minimax(board, player_choice.get())
        else:
            score, _ = minimax(board, ai_player)
        board[row][col] = " "
        moves.append((score, (row, col)))

    if player == ai_player:
        best_score, best_move = max(moves, key=lambda x: x[0])
    else:
        best_score, best_move = min(moves, key=lambda x: x[0])

    return best_score, best_move

def easy_ai(board, player):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
    return 0, random.choice(empty_cells)

def normal_ai(board, player):
    # Check if the AI can win in the next move
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = player
                if check_win(board, player):
                    board[row][col] = " "
                    return 1, (row, col)
                board[row][col] = " "

    # Check if the opponent can win in the next move and block it
    opponent = "X" if player == "O" else "O"
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = opponent
                if check_win(board, opponent):
                    board[row][col] = " "
                    return -1, (row, col)
                board[row][col] = " "

    # If no immediate win or block, choose a random available move
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
    return 0, random.choice(empty_cells)

def on_difficulty_change(event):
    global ai_difficulty
    ai_difficulty = difficulty_combobox.get()

def toggle_fullscreen(event=None):
    global fullscreen_mode
    fullscreen_mode = not fullscreen_mode
    root.attributes('-fullscreen', fullscreen_mode)
    
    if fullscreen_mode:
        root.geometry("")  # Clear the geometry to use fullscreen dimensions
    else:
        root.geometry("400x400")  # Set your preferred window size here

    # Center the board on the window
    root.update_idletasks()  # Ensure the window dimensions are updated
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    board_width = sum(buttons[0][col].winfo_width() for col in range(3))
    board_height = sum(buttons[row][0].winfo_height() for row in range(3))
    x_offset = (window_width - board_width) // 2
    y_offset = (window_height - board_height) // 2

    for row in range(3):
        for col in range(3):
            buttons[row][col].place(x=x_offset + col * buttons[row][col].winfo_width(),
                                    y=y_offset + row * buttons[row][col].winfo_height())

def start_game():
    global current_player
    current_player = player_choice.get()

    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state=tk.NORMAL)

    difficulty_combobox.config(state=tk.DISABLED)  # Disable difficulty selection after starting
    start_button.config(state=tk.DISABLED)  # Disable the "Start" button after starting

    if current_player == ai_player:
        make_ai_move()

root = tk.Tk()
root.title("Tic-Tac-Toe")

fullscreen_mode = False

# Create a Combobox to select AI difficulty
ai_difficulty = "Easy"
difficulty_combobox = ttk.Combobox(root, values=["Easy", "Normal", "Minimax"])
difficulty_combobox.grid(row=4, columnspan=3, pady=10)
difficulty_combobox.set(ai_difficulty)
difficulty_combobox.bind("<<ComboboxSelected>>", on_difficulty_change)  # Bind the selection event

board = [[" " for _ in range(3)] for _ in range(3)]
player_choice = tk.StringVar()
player_choice.set("X")  # Default choice
current_player = player_choice.get()
game_over = False
ai_player = "O" if current_player == "X" else "X"

style = ttk.Style()
style.configure("TButton", padding=10, font=("Arial", 14))

buttons = [[None, None, None], [None, None, None], [None, None, None]]

for row in range(3):
    for col in range(3):
        buttons[row][col] = ttk.Button(root, text=" ", width=10, command=lambda row=row, col=col: on_click(row, col))
        buttons[row][col].grid(row=row, column=col)

reset_button = ttk.Button(root, text="Reset", command=reset_board)
reset_button.grid(row=3, column=1, pady=10)

player_choice_label = tk.Label(root, text="Choose X or O:", font=("Arial", 14))
player_choice_label.grid(row=3, column=0, pady=10)
player_choice_radio_x = ttk.Radiobutton(root, text="X", variable=player_choice, value="X", command=reset_board)
player_choice_radio_x.grid(row=3, column=2, pady=10)
player_choice_radio_o = ttk.Radiobutton(root, text="O", variable=player_choice, value="O", command=reset_board)
player_choice_radio_o.grid(row=3, column=3, pady=10)

# Add a "Start" button
start_button = ttk.Button(root, text="Start", command=start_game)
start_button.grid(row=5, columnspan=3, pady=10)

# Add a "Fullscreen" button
fullscreen_button = ttk.Button(root, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.grid(row=6, columnspan=3, pady=10)

root.mainloop()
