from tkinter import *
import random
from tkinter import messagebox

from PIL import ImageTk, Image
import keyboard

x_pos = 4
y_pos = 0
score = 0

game_grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# gold -> 1, lava -> 2, gas -> 3
block_type = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

block_message = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]


def generate_map():
    # choose gold position
    gold_row = random.randint(0, 3)
    gold_column = random.randint(2, 4)
    block_type[gold_row][gold_column] = 1
    lava = 0
    for row in range(5):
        for column in range(5):
            random_nr = random.randint(1, 10)
            if block_type[row][column] == 0 and row != 4 and column != 0:
                if random_nr % 4 == 0 and lava < 4:
                    block_type[row][column] = 2
                    lava += 1
                elif random_nr == 9:
                    block_type[row][column] = 3


def reset_game():
    for row in range(5):
        for column in range(5):
            block_message[row][column] = 0
            block_type[row][column] = 0
            game_grid[row][column].configure(background='burlywood4', image='', borderwidth=1)

    generate_map()
    generate_block_messages()

    global x_pos, y_pos, score
    score = 0
    x_pos = 4
    y_pos = 0
    score_lbl.configure(text="Score: " + str(score))
    game_grid[x_pos][y_pos].configure(borderwidth=3, image=msg_to_pic(block_message[x_pos][y_pos]))


def key_pressed(event, window, score_lbl):
    global x_pos, y_pos, score
    if event.char == "w":
        game_grid[x_pos][y_pos].configure(borderwidth=1)
        if x_pos > 0:
            x_pos = x_pos - 1
    elif event.char == "s":
        game_grid[x_pos][y_pos].configure(borderwidth=1)
        if x_pos < 4:
            x_pos = x_pos + 1
    elif event.char == "d":
        game_grid[x_pos][y_pos].configure(borderwidth=1)
        if y_pos < 4:
            y_pos = y_pos + 1
    elif event.char == "a":
        game_grid[x_pos][y_pos].configure(borderwidth=1)
        if y_pos > 0:
            y_pos = y_pos - 1

    game_grid[x_pos][y_pos].configure(borderwidth=3, image=msg_to_pic(block_message[x_pos][y_pos]))
    if block_type[x_pos][y_pos] == 2:
        resp = messagebox.askquestion('Game Over', 'Do you want to play again?')
        if resp == 'no':
            window.after(1000, lambda: window.destroy())
        else:
            reset_game()
    elif block_type[x_pos][y_pos] == 1:
        score += 100
        score_lbl.configure(text="Score: " + str(score))
        resp = messagebox.askquestion('You found the gold! Score: ' + str(score), 'Do you want to play again?')
        if resp == 'no':
            window.after(1000, lambda: window.destroy())
        else:
            reset_game()
    elif block_type[x_pos][y_pos] == 3:
        score -= 15
        score_lbl.configure(text="Score: " + str(score))
    else:
        score -= 5
        score_lbl.configure(text="Score: " + str(score))


def create_start_window():
    window = Tk()
    window.title("Gold-digging game")
    window.geometry("800x600")
    window.resizable(False, False)
    window.configure(background='#84c497')
    window_title = Label(text="Dig for gold!", font=('consolas', 30), background='#84c497')
    window_title.pack(side=TOP)
    window.bind("<Key>", lambda e: key_pressed(e, window, score_lbl))
    return window


def get_neighbours(x, y):
    neighbours = []
    if x >= 1:
        up = (x - 1, y)
        neighbours.append(up)
    if x <= 3:
        down = (x + 1, y)
        neighbours.append(down)
    if y <= 3:
        right = (x, y + 1)
        neighbours.append(right)
    if y >= 1:
        left = (x, y - 1)
        neighbours.append(left)

    return neighbours


def generate_block_messages():
    for row in range(5):
        for column in range(5):
            neigh = get_neighbours(row, column)

            if block_type[row][column] == 2:
                block_message[row][column] = "LAVA"
                for x, y in neigh:
                    if block_type[x][y] == 0:
                        block_message[x][y] = (str(block_message[x][y]) + "HEAT")

            elif block_type[row][column] == 3:
                block_message[row][column] = "GAS HERE"
                for x, y in neigh:
                    if block_type[x][y] == 0:
                        block_message[x][y] = (str(block_message[x][y]) + "GAS")

            elif block_type[row][column] == 1:
                block_message[row][column] = "GOLD"

            else:
                block_message[row][column] = (str(block_message[row][column]) + "EMPTY")


def msg_to_pic(msg):
    if msg == "LAVA":
        return lava_img
    elif msg == "GAS HERE":
        return gas_img
    elif msg == "GOLD":
        return gold_img
    elif str(msg).__contains__("HEAT") and not str(msg).__contains__("GAS"):
        return heat_msg_img
    elif str(msg).__contains__("GAS") and not str(msg).__contains__("HEAT"):
        return gas_msg_img
    elif str(msg).__contains__("HEAT") and str(msg).__contains__("GAS"):
        return heat_gas_msg_img
    else:
        return empty_msg_img


if __name__ == "__main__":
    window = create_start_window()
    frame = Frame(window, background='#84c497')
    frame.pack()
    for row in range(5):
        for column in range(5):
            game_grid[row][column] = Label(frame, padx=70, pady=40, borderwidth=1,
                                           relief="solid", background='burlywood4')
            game_grid[row][column].grid(row=row, column=column)

    generate_map()
    generate_block_messages()

    gold_img = ImageTk.PhotoImage(Image.open("gold.png").resize((150, 100), Image.Resampling.LANCZOS))
    lava_img = ImageTk.PhotoImage(Image.open("lava.png").resize((150, 100), Image.Resampling.LANCZOS))
    gas_img = ImageTk.PhotoImage(Image.open("gas.png").resize((150, 100), Image.Resampling.LANCZOS))
    heat_msg_img = ImageTk.PhotoImage(Image.open("heat_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    gas_msg_img = ImageTk.PhotoImage(Image.open("gas_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    heat_gas_msg_img = ImageTk.PhotoImage(
        Image.open("heat_gas_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    empty_msg_img = ImageTk.PhotoImage(Image.open("empty_message.png").resize((150, 100), Image.Resampling.LANCZOS))

    game_grid[x_pos][y_pos].configure(borderwidth=3, image=msg_to_pic(block_message[x_pos][y_pos]))

    score_lbl = Label(text="Score: 0", font=('consolas', 30), background='#84c497')
    score_lbl.pack(side=BOTTOM)

    window.mainloop()
