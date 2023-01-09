import os
import tkinter as tk
import random
import numpy as np
import itertools as it
from PIL import ImageTk, Image

def valid_game(cards, row, col, images_per_card):
    # print(cards)
    # check that there are no repeats in the row
    if len(set(cards[row]) - {0}) != (col + 1):
        print("CARD WITH DUPLICATE")
        print(cards[row])
        return False
    
    for card in range(row):
        # check that the intersection is at most 1
        if col < (images_per_card - 1):
            if len((set(cards[card]) - {0}).intersection(cards[row])) > 1:
                print("MATHCHING CARDS:")
                print(cards[card])
                print(cards[row])
                return False
        else:
        # if it's the last column check that the intersection is EXACTLY 1
            if len((set(cards[card]) - {0}).intersection(cards[row])) != 1:
                print("VIOLATING CARDS:")
                print(cards[card])
                print(cards[row])
                return False

    return True


def create_cards(cards, num_symbols):
    _ , images_per_card = cards.shape
    zeros = np.where(cards == 0)
    # print(f"{round(100 * np.mean(cards != 0), 2)}%")
    if len(zeros[0]) > 0:
        row_val, col_val = zeros[0][0], zeros[1][0]
    else:
        return cards
    for value in range((images_per_card - 1) * col_val + 2, (images_per_card - 1) * col_val + 2 + (images_per_card - 1)):
        cards[row_val, col_val] = value
        if valid_game(cards, row_val, col_val, images_per_card):
            if isinstance(create_cards(cards, num_symbols), np.ndarray):
                return cards
        print(f"BACKTRACK: {row_val}, {col_val}")
        cards[row_val, col_val] = 0
    return False


def generate_cards(num_cards=57, num_symbols=57, images_per_card=8):

    if f"{images_per_card}x{images_per_card}.txt" in os.listdir('layouts'):
        full_deck = np.loadtxt(f"layouts/{images_per_card}x{images_per_card}.txt", dtype='int')
        return full_deck[:num_cards]

    if num_cards > num_symbols:
        raise ValueError("Not enough symbols for game of this size.")
    # BACKTRACKING ALGORITHM
    cards = np.zeros((num_cards, images_per_card), dtype=int)
    # set all the free variables (i.e. generate all the cards with image #1) 
    cards[:, 0] = [1] + [x for x in range(1, images_per_card + 1) for _ in range(images_per_card-1)]
    for i in range(images_per_card):
        cards[i][1:] = np.arange(2, images_per_card + 1) + (images_per_card - 1) * i
    cards[images_per_card:, 1] = np.tile(cards[1][1:], (images_per_card - 1))
    # POSSIBLE O(N) SOLUTION
    zeros = np.where(cards == 0)
    for x, y in zip(zeros[0], zeros[1]):
        possible_value = cards[x][y-1] + ((images_per_card - 1) + (cards[x][0] - 2))
        # print(possible_value, )
        if possible_value - cards[y][-1] > 0:
            cards[x][y] = cards[y][possible_value - cards[y][-1]] - (images_per_card - 1) * (possible_value - cards[y][-1] > cards[y][-1])
        else:
            cards[x][y] = possible_value
    # print(cards)
    return create_cards(cards, num_symbols)

def update_card(window, cards, you, game_images, label_dict, image_dict, image):

    # get window width
    window_width = window.winfo_reqwidth()

    # set up superpixels
    print(window_width)
    superpixels = {
        1: [(0.05 * window_width + 45, 0.4 * window_width), (0.1 * window_width + 22.5, 0.45 * window_width - 22.5), (0.1 * window_width + 22.5, 0.35 * window_width + 22.5), (0.15 * window_width, 0.5 * window_width - 45), (0.15 * window_width, 0.4 * window_width), (0.15 * window_width, 0.3 * window_width + 45), (0.2 * window_width - 22.5, 0.45 * window_width - 22.5), (0.2 * window_width - 22.5, 0.35 * window_width + 22.5), (0.25 * window_width - 45, 0.4 * window_width)],
        2: [(0.75 * window_width + 45, 0.4 * window_width), (0.8 * window_width + 22.5, 0.45 * window_width - 22.5), (0.8 * window_width + 22.5, 0.35 * window_width + 22.5), (0.85 * window_width, 0.5 * window_width - 45), (0.85 * window_width, 0.4 * window_width), (0.85 * window_width, 0.3 * window_width + 45), (0.9 * window_width - 22.5, 0.45 * window_width - 22.5), (0.9 * window_width - 22.5, 0.35 * window_width + 22.5), (0.95 * window_width - 45, 0.4 * window_width)]
    }

    # check if the game is over
    if len(cards) == 0:
        if you:
            for k, _ in image_dict[1].items():
                label_dict[1][k].destroy()
            label = tk.Label(text='YOU WIN!')
            label.place(x = 0.15 * window_width, y = 0.4 * window_width, anchor='s')
        else:
            for k, _ in image_dict[2].items():
                label_dict[2][k].destroy()
            label = tk.Label(text='The AI beat you.')
            label.place(x = 0.85 * window_width, y = 0.4 * window_width, anchor='s')
        return "Game Finished"

    new_card_index = np.random.choice(cards.shape[0], size=1, replace=False)
    new_card = cards[new_card_index]
    cards = np.delete(cards, new_card_index, axis=0)

    images = set(new_card[0])
    # remove self edge
    images.discard(-1)

    # check if the image is in the center card
    if image not in [image_dict[0][j][1] for j in range(len(images))]:
        return cards

    # change the image
    # Question: Why don't I need to destroy center buttons?
    i = 1 if you else 2
    for k, _ in image_dict[i].items():
        image_dict[0][k] = image_dict[i][k]
        label_dict[0][k] = tk.Button(image=image_dict[0][k][0], bd=0, bg="white", relief='sunken', command=tk.DISABLED)
        label_dict[0][k].place(x = label_dict[i][k].winfo_rootx() + 0.35 * (-np.sign(i - 1.5)) * window_width - 10, y = label_dict[i][k].winfo_rooty() - 0.3 * window_width - 20)
        label_dict[i][k].destroy()
    for j, image in enumerate(images):
        raw_image = Image.open("game_images/" + game_images[image - 1])
        transformed_image = raw_image.resize((np.random.randint(30, 80),)*2).rotate(np.random.uniform(0, 360))
        # create new button and move the old button to the center
        image_dict[i][j] = (ImageTk.PhotoImage(transformed_image), image)
        label_dict[i][j] = tk.Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards, bool(i-2), game_images, label_dict = label_dict, image_dict = image_dict, image = image))
        # select a random superpixel upon which to place the new image
        random_index = np.random.choice(len(superpixels[i]), size=1, replace=False)[0]
        x, y = superpixels[i][random_index]
        superpixels[i].pop(random_index)
        label_dict[i][j].place(x=x , y=y, anchor="center")

    return cards 

def launch_game(window_width=1250):

    # generate the cards
    cards = generate_cards(num_cards=57, num_symbols=57, images_per_card=8)

    # get the images
    game_images = os.listdir("game_images")

    # declare the window
    window = tk.Tk()
    # set window title
    window.title("Spot It!")
    # set window width and height (originally)
    window.configure(width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    # set window background color
    window.configure(bg='white')

    # Create a canvas object
    window_width, window_height = window.winfo_reqwidth(), window.winfo_reqheight()
    c = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(), bg="white")
    c.pack()

    # Draw an Oval in the canvas
    c.create_oval(0.4 * window_width, 10 , 0.6 * window_width, 10 + 0.2 * window_width)

    # Your card
    c.create_oval(0.05 * window_width, 0.3 * window_width , 0.25 * window_width, 0.5 * window_width)
    # AI's card
    c.create_oval(0.75 * window_width, 0.3 * window_width , 0.95 * window_width, 0.5 * window_width)

    # create user labels
    c.create_window(0.15 * window_width, 0.5 * window_width + 30, window=tk.Label(text="You", width=10, height=2))
    c.create_window(0.85 * window_width, 0.5 * window_width + 30, window=tk.Label(text="AI", width=10, height=2))

    # set up superpixels
    print(window_width)
    superpixels = {
        0: [(0.05 * window_width + 90, 0.4 * window_width), (0.1 * window_width + 45, 0.45 * window_width - 45), (0.1 * window_width + 45, 0.35 * window_width + 45), (0.15 * window_width, 0.5 * window_width - 90), (0.15 * window_width, 0.4 * window_width), (0.15 * window_width, 0.3 * window_width + 90), (0.2 * window_width - 45, 0.45 * window_width - 45), (0.2 * window_width - 45, 0.35 * window_width + 45), (0.25 * window_width - 90, 0.4 * window_width)],
        1: [(0.05 * window_width + 45, 0.4 * window_width), (0.1 * window_width + 22.5, 0.45 * window_width - 22.5), (0.1 * window_width + 22.5, 0.35 * window_width + 22.5), (0.15 * window_width, 0.5 * window_width - 45), (0.15 * window_width, 0.4 * window_width), (0.15 * window_width, 0.3 * window_width + 45), (0.2 * window_width - 22.5, 0.45 * window_width - 22.5), (0.2 * window_width - 22.5, 0.35 * window_width + 22.5), (0.25 * window_width - 45, 0.4 * window_width)],
        2: [(0.75 * window_width + 45, 0.4 * window_width), (0.8 * window_width + 22.5, 0.45 * window_width - 22.5), (0.8 * window_width + 22.5, 0.35 * window_width + 22.5), (0.85 * window_width, 0.5 * window_width - 45), (0.85 * window_width, 0.4 * window_width), (0.85 * window_width, 0.3 * window_width + 45), (0.9 * window_width - 22.5, 0.45 * window_width - 22.5), (0.9 * window_width - 22.5, 0.35 * window_width + 22.5), (0.95 * window_width - 45, 0.4 * window_width)]
    }

    # WORKFLOW

    # initialize game
    starting_card_indeces = np.random.choice(cards.shape[0], size=3, replace=False)
    starting_cards = cards[starting_card_indeces]
    cards = np.delete(cards, starting_card_indeces, axis=0)
    cards_you = cards[np.random.choice(cards.shape[0], size=len(cards)//2, replace=False)]
    cards_AI = cards[np.random.choice(cards.shape[0], size=len(cards)//2, replace=False)]

    assert len(cards_you) == len(cards_AI)
    # print(f"You and the AI both have {len(cards_you + 1)} cards.")

    image_dict = {}
    label_dict = {}
    for i, card in enumerate(starting_cards):
        images = set(card)
        # remove self edge
        images.discard(-1)
        image_dict[i] = {}
        label_dict[i] = {}
        for j, image in enumerate(images):
            raw_image = Image.open("game_images/" + game_images[image - 1])
            transformed_image = raw_image.resize((np.random.randint(30, 80),)*2).rotate(np.random.uniform(0, 360))
            # dictionary assignment doesn't overwrite buttons and they all get saved
            image_dict[i][j] = (ImageTk.PhotoImage(transformed_image), image)
            random_index = np.random.choice(len(superpixels[i]), size=1, replace=False)[0]
            x, y = superpixels[i][random_index]
            superpixels[i].pop(random_index)
            if i == 0:
                label_dict[i][j] = tk.Button(image=image_dict[i][j][0], bd=0, bg="white", relief='sunken', command=tk.DISABLED)
            if i == 1:
                label_dict[i][j] = tk.Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards_you, True, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
            if i == 2:
                label_dict[i][j] = tk.Button(image=image_dict[i][j][0], bd=0, bg="white", command = lambda image=image: update_card(window, cards_AI, False, game_images, label_dict = label_dict, image_dict = image_dict, image = image))
            label_dict[i][j].place(x=x , y=y, anchor="center")
    
    window.mainloop()

if __name__ == "__main__":
    launch_game()
    # import time
    # time_dict = {}
    # for i in range(3,25):
    #     if i == 7:
    #         continue
    #     start = time.time()
    #     layout = generate_cards(num_cards = i**2 - i + 1, num_symbols=i ** 2 - i + 1, images_per_card=i)
    #     # print(layout)
    #     if not os.path.exists(f'layouts/{i}x{i}.txt') and valid_game(layout, row=i**2 - i, col=i-1, images_per_card=i):
    #         np.savetxt(f'layouts/{i}x{i}.txt', layout, fmt="%i")
    #     end = time.time()
    #     time_dict[i] = end - start
    #     print(i, ": ", valid_game(layout, row=i**2 - i, col=i-1, images_per_card=i))
    # layout = np.loadtxt('layouts/9x9.txt')
    # print(9, ": ", valid_game(layout, row=72, col=8, images_per_card=i))
    # layout = np.loadtxt('layouts/5x5.txt')
    # print(5, ": ", valid_game(layout, row=20, col=4, images_per_card=i))
    # print(time_dict)