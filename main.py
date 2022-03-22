import random
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"
TIME_OF_FLIP = 3000
current_word = {}
for_learning = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv.csv")
except FileNotFoundError:
    og_data = pandas.read_csv("data/french_words.csv")
    for_learning = og_data.to_dict(orient="record")
else:
    for_learning = data.to_dict(orient="record")


def next_card():
    """Displays the card"""
    global current_word, flip_timer
    window.after_cancel(flip_timer)  # to prevent the counter from counting in the background or
    current_word = random.choice(for_learning)
    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    card_canvas.itemconfig(canvas_background, image=card_front)
    flip_timer = window.after(TIME_OF_FLIP, func=flip_card)


def is_known():
    """removes the words that the user deems as known and saves the remaining unlearnt words
    inside data/words_to_learn"""
    for_learning.remove(current_word)
    data = pandas.DataFrame(for_learning)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    """Display the back side (the answer side) of the card"""
    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(card_word, text=current_word["English"], fill="white")
    card_canvas.itemconfig(canvas_background, image=card_back)


#  WINDOW
window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.minsize(height=700, width=900)
window.maxsize(height=700, width=900)
flip_timer = window.after(TIME_OF_FLIP, func=flip_card)

# CANVAS
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
right = PhotoImage(file="./images/right.png")
unknown = PhotoImage(file="./images/wrong.png")

# Card Canvas
card_canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas_background = card_canvas.create_image(400, 263,image=card_back)
card_canvas.config(bg=BACKGROUND_COLOR)
card_title = card_canvas.create_text(400, 150, text="", font=("Fira sans", 20, "italic"))
card_word = card_canvas.create_text(400, 250, text="", font=("Fira sans", 25, "bold"))
card_canvas.grid(column=0, row=0, columnspan=2)

# Unknown Button
unknown_btn = Button(image=unknown, highlightthickness=0, command=next_card)
unknown_btn.grid(column=0, row=1)

# Right Button
right_btn = Button(image=right, highlightthickness=0, command=is_known)
right_btn.grid(column=1, row=1)


next_card()


window.mainloop()

