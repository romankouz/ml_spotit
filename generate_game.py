import os, sys
import numpy as np
import itertools as it
from tkinter import *
from PIL import ImageTk, Image

def generate_cards(num_cards=55, num_symbols=57, images_per_card=8):
    similarities = np.zeros((num_cards, num_cards))
    for symbol in range(num_symbols):
        pass

    # Could 0s be replaced with _ and automatically ignored by the set?
    cards = np.array([
        [0,1,1,1,2,2,2,3,3,3,4,4,4],
        [1,0,1,1,5,6,7,5,6,7,5,6,7],
        [1,1,0,1,8,9,10,9,10,8,10,8,9],
        [1,1,1,0,11,12,13,13,11,12,12,13,11],
        [2,5,8,11,0,2,2,5,11,8,5,8,11],
        [2,6,9,12,2,0,2,9,6,12,12,6,9],
        [2,7,10,13,2,2,0,13,10,7,10,13,7],
        [3,5,9,13,5,9,13,0,3,3,5,13,9],
        [3,6,10,11,11,6,10,3,0,3,10,6,11],
        [3,7,8,12,8,12,7,3,3,0,12,8,7],
        [4,5,10,12,5,12,10,5,10,12,0,4,4],
        [4,6,8,13,8,6,13,13,6,8,4,0,4],
        [4,7,9,11,11,9,7,9,11,7,4,4,0]
    ])

    for row in range(len(cards)):
        for other_row in range(row + 1, len(cards)):
            # 2 because of the match to itself and 1 other card
           assert len(set(cards[row]).intersection(set(cards[other_row]))) == 2
    print("This game is valid!")

    # script should assign numbers to a particular image

    return cards

def update_card(window, cards, you, game_images, label_dict, image_dict, image):

    print(label_dict)

    # get window width
    window_width = window.winfo_reqwidth()

    # check if the game is over
    if len(cards) == 0:
        if you:
            for k, _ in image_dict[1].items():
                label_dict[1][k].destroy()
            label = Label(text='YOU WIN!')
            label.place(x = 0.15 * window_width, y = 0.4 * window_width, anchor='s')
        else:
            for k, _ in image_dict[2].items():
                label_dict[2][k].destroy()
            label = Label(text='The AI beat you.')
            label.place(x = 0.85 * window_width, y = 0.4 * window_width, anchor='s')
        return "Game Finished"

    new_card_index = np.random.choice(cards.shape[0], size=1, replace=False)
    new_card = cards[new_card_index]
    print(new_card)
    cards = np.delete(cards, new_card_index, axis=0)

    images = set(new_card[0])
    # remove self edge
    images.discard(0)

    # check if the image is in the center card
    if image not in [image_dict[0][j][1] for j in range(len(images))]:
        return cards

    # change the image
    # FIX THIS SO THAT THIS CODE IS ONLY WRITTEN ONCE
    # Question: Why don't I need to destroy center buttons?
    if you:
        i = 1
        for k, _ in image_dict[i].items():
            image_dict[0][k] = image_dict[i][k]
            label_dict[0][k] = Button(image=image_dict[0][k][0], bd=0, bg="white", relief='sunken', command=DISABLED)
            label_dict[0][k].place(x = label_dict[i][k].winfo_rootx() + 0.35 * window_width - 10, y = label_dict[i][k].winfo_rooty() - 0.3 * window_width - 20)
            label_dict[i][k].destroy()
        for j, image in enumerate(images):
            raw_image = Image.open("game_images/" + game_images[image - 1])
            transformed_image = raw_image.resize((np.random.randint(30, 90),)*2).rotate(np.random.uniform(0, 360))
            # create new button and move the old button to the center
            image_dict[i][j] = (ImageTk.PhotoImage(transformed_image), image)
            label_dict[i][j] = Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards, True, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
            label_dict[i][j].place(x=np.random.uniform(0.1 * window_width,  0.2 * window_width), y=np.random.uniform(0.35 * window_width, 0.45 * window_width))
    
    else:
        i = 2
        for k, _ in image_dict[i].items():
            label_dict[i][k].destroy()
        for j, image in enumerate(images):
            raw_image = Image.open("game_images/" + game_images[image - 1])
            transformed_image = raw_image.resize((np.random.randint(30, 90),)*2).rotate(np.random.uniform(0, 360))
            # dictionary assignment doesn't overwrite buttons and they all get saved
            image_dict[i][j] = (ImageTk.PhotoImage(transformed_image), image)
            label_dict[i][j] = Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards, False, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
            label_dict[i][j].place(x=np.random.uniform(0.8 * window_width,  0.9 * window_width), y=np.random.uniform(0.35 * window_width, 0.45 * window_width))

    print("Button was clicked.")
    return cards
    

def launch_game(window_width=1250, window_height=750):

    # generate the cards
    cards = generate_cards()

    # get the images
    game_images = os.listdir("game_images")

    # declare the window
    window = Tk()
    # set window title
    window.title("Spot It!")
    # set window width and height (originally)
    window.configure(width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    # set window background color
    window.configure(bg='white')

    # Create a canvas object
    window_width, window_height = window.winfo_reqwidth(), window.winfo_reqheight()
    c = Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(), bg="white")
    c.pack()

    # Draw an Oval in the canvas
    
    print(window_width, window_height)
    c.create_oval(0.4 * window_width, 10 , 0.6 * window_width, 10 + 0.2 * window_width)

    # Your card
    c.create_oval(0.05 * window_width, 0.3 * window_width , 0.25 * window_width, 0.5 * window_width)
    # AI's card
    c.create_oval(0.75 * window_width, 0.3 * window_width , 0.95 * window_width, 0.5 * window_width)

    # create user labels
    c.create_window(0.15 * window_width, 0.5 * window_width + 30, window=Label(text="You", width=10, height=2))
    c.create_window(0.85 * window_width, 0.5 * window_width + 30, window=Label(text="AI", width=10, height=2))

    # WORKFLOW

    # initialize game
    starting_card_indeces = np.random.choice(cards.shape[0], size=3, replace=False)
    starting_cards = cards[starting_card_indeces]
    print(starting_cards)
    cards = np.delete(cards, starting_card_indeces, axis=0)
    cards_you = cards[np.random.choice(cards.shape[0], size=len(cards)//2, replace=False)]
    cards_AI = cards[np.random.choice(cards.shape[0], size=len(cards)//2, replace=False)]

    assert len(cards_you) == len(cards_AI)
    print(f"You and the AI both have {len(cards_you + 1)} cards.")

    image_dict = {}
    label_dict = {}
    for i, card in enumerate(starting_cards):
        images = set(card)
        # remove self edge
        images.discard(0)
        image_dict[i] = {}
        label_dict[i] = {}
        for j, image in enumerate(images):
            raw_image = Image.open("game_images/" + game_images[image - 1])
            transformed_image = raw_image.resize((np.random.randint(30, 90),)*2).rotate(np.random.uniform(0, 360))
            # dictionary assignment doesn't overwrite buttons and they all get saved
            image_dict[i][j] = (ImageTk.PhotoImage(transformed_image), image)
            if i == 0:
                label_dict[i][j] = Button(image=image_dict[i][j][0], bd=0, bg="white", relief='sunken', command=DISABLED)
                label_dict[i][j].place(x=np.random.uniform(0.45 * window_width,  0.55 * window_width), y=np.random.uniform(10 + 0.05 * window_width, 10 + 0.15 * window_width))
            if i == 1:
                label_dict[i][j] = Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards_you, True, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
                label_dict[i][j].place(x=np.random.uniform(0.1 * window_width,  0.2 * window_width), y=np.random.uniform(0.35 * window_width, 0.45 * window_width))
            if i == 2:
                label_dict[i][j] = Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards_AI, False, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
                label_dict[i][j].place(x=np.random.uniform(0.8 * window_width,  0.9 * window_width), y=np.random.uniform(0.35 * window_width, 0.45 * window_width))
    
    window.mainloop()

if __name__ == "__main__":
    launch_game()