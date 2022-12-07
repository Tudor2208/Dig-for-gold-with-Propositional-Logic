from tkinter import *
import random
from tkinter import messagebox
from nltk.test.inference_fixt import setup_module
from nltk import *
from nltk.sem.drt import DrtParser
from nltk.sem import logic
from nltk.sem import Expression

from PIL import ImageTk, Image
import keyboard

x_pos = 4
y_pos = 0
score = 0
safe_pos_string = "Safe positions: "

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

read_expr = Expression.fromstring
rules = []
assumptions = []


def get_rules_from_file(file_name):
    rules = []
    with open(file_name, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if not line.isspace():
                rules.append(read_expr(line))

    return rules


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
                if random_nr % 4 == 0 and lava < 5:
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
    assumptions.clear()
    assumptions.extend(rules)

    global x_pos, y_pos, score, safe_pos_string
    score = 0
    x_pos = 4
    y_pos = 0
    score_lbl.configure(text="Score: " + str(score))
    game_grid[x_pos][y_pos].configure(borderwidth=3, image=msg_to_pic(block_message[x_pos][y_pos]))

    safe_pos_lbl.configure(text=safe_pos_string)
    safe_pos_string = "Safe positions: "


def key_pressed(event, window, score_lbl):
    global x_pos, y_pos, score, safe_pos_string
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

    my_image = msg_to_pic(block_message[x_pos][y_pos])
    game_grid[x_pos][y_pos].configure(borderwidth=3, image=my_image)
    if my_image == gas_msg_img:
        assumptions.append(read_expr('GN' + str(x_pos) + str(y_pos)))
    elif my_image == heat_msg_img:
        assumptions.append(read_expr('H' + str(x_pos) + str(y_pos)))
    elif my_image == heat_gas_msg_img:
        assumptions.append(read_expr('H' + str(x_pos) + str(y_pos)))
        assumptions.append(read_expr('GN' + str(x_pos) + str(y_pos)))
    elif my_image == empty_msg_img:
        assumptions.append(read_expr('E' + str(x_pos) + str(y_pos)))

    if block_type[x_pos][y_pos] == 2:
        resp = messagebox.askquestion('Game Over', 'Do you want to play again?')
        if resp == 'no':
            window.after(1000, lambda: window.destroy())
        else:
            reset_game()
    elif block_type[x_pos][y_pos] == 1:
        score += 500
        score_lbl.configure(text="Score: " + str(score))
        resp = messagebox.askquestion('You found the gold! Congratulations!', 'Do you want to play again?')
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

    x_1 = x_pos - 1
    x_1_plus = x_pos + 1
    y_1 = y_pos - 1
    y_1_plus = y_pos + 1

    if x_1 >= 0:
        g1 = read_expr('-G' + str(x_1) + str(y_pos) + ' & -L' + str(x_1) + str(
            y_pos))  # UP is safe
        if Prover9().prove(g1, assumptions):
            safe_pos_string += "UP "
    if x_1_plus <= 4:
        g2 = read_expr('-G' + str(x_1_plus) + str(y_pos) + ' & -L' + str(x_1_plus) + str(
            y_pos))  # DOWN is safe
        if Prover9().prove(g2, assumptions):
            safe_pos_string += "DOWN "
    if y_1_plus <= 4:
        g3 = read_expr('-G' + str(x_pos) + str(y_1_plus) + ' & -L' + str(x_pos) + str(
            y_1_plus))  # RIGHT is safe
        if Prover9().prove(g3, assumptions):
            safe_pos_string += "RIGHT "
    if y_1 >= 0:
        g4 = read_expr('-G' + str(x_pos) + str(y_1) + ' & -L' + str(x_pos) + str(
            y_1))  # LEFT is safe
        if Prover9().prove(g4, assumptions):
            safe_pos_string += "LEFT"

    safe_pos_lbl.configure(text=safe_pos_string)
    safe_pos_string = "Safe positions: "


def create_start_window():
    window = Tk()
    window.title("Gold-digging game")
    window.geometry("800x650")
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
    rules = get_rules_from_file("rules.txt")
    assumptions.extend(rules)

    gold_img = ImageTk.PhotoImage(Image.open("gold.png").resize((150, 100), Image.Resampling.LANCZOS))
    lava_img = ImageTk.PhotoImage(Image.open("lava.png").resize((150, 100), Image.Resampling.LANCZOS))
    gas_img = ImageTk.PhotoImage(Image.open("gas.png").resize((150, 100), Image.Resampling.LANCZOS))
    heat_msg_img = ImageTk.PhotoImage(Image.open("heat_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    gas_msg_img = ImageTk.PhotoImage(Image.open("gas_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    heat_gas_msg_img = ImageTk.PhotoImage(
        Image.open("heat_gas_message.png").resize((150, 100), Image.Resampling.LANCZOS))
    empty_msg_img = ImageTk.PhotoImage(Image.open("empty_message.png").resize((150, 100), Image.Resampling.LANCZOS))

    game_grid[x_pos][y_pos].configure(borderwidth=3, image=msg_to_pic(block_message[x_pos][y_pos]))
    score_lbl = Label(text="Score: 0", font=('consolas', 30), background='#84c497', fg='#94091e')
    score_lbl.pack(side=BOTTOM)

    x = 4
    y = 0
    my_image = msg_to_pic(block_message[x][y])
    game_grid[x][y].configure(borderwidth=3, image=my_image)
    if my_image == gas_msg_img:
        assumptions.append(read_expr('GN' + str(x) + str(y)))
    elif my_image == heat_msg_img:
        assumptions.append(read_expr('H' + str(x) + str(y)))
    elif my_image == heat_gas_msg_img:
        assumptions.append(read_expr('H' + str(x) + str(y)))
        assumptions.append(read_expr('GN' + str(x) + str(y)))
    elif my_image == empty_msg_img:
        assumptions.append(read_expr('E' + str(x) + str(y)))

    goal_1 = read_expr('-G' + str(x-1) + str(y) + ' & -L' + str(x-1) + str(
        y))  # UP is safe
    if Prover9().prove(goal_1, assumptions):
        safe_pos_string += "UP "

    goal_2 = read_expr('-G' + str(x) + str(y+1) + ' & -L' + str(x) + str(
        y+1))  # RIGHT is safe
    if Prover9().prove(goal_2, assumptions):
        safe_pos_string += "RIGHT "

    safe_pos_lbl = Label(text=safe_pos_string, font=('consolas', 25), background='#84c497', fg='#5534eb')
    safe_pos_string = "Safe positions: "
    safe_pos_lbl.pack(side=BOTTOM)

    window.mainloop()


