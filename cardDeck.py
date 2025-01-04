from tkinter import *
import random
from PIL import Image, ImageTk

root = Tk()
root.title('BlackJack')
root.geometry("1000x500")
root.configure(backgroun = "green")


def resize_image(image):
    img = Image.open(image)
    img_resize = img.resize((75, 109))
    global card_image
    card_image = ImageTk.PhotoImage(img_resize)
    return card_image

def update_scores():
    """Update the score labels for both dealer and player."""
    dealer_frame.config(text=f"Dealer - Score: {dealer_value if len(dealer) > 2 else '?'}")
    player_frame.config(text=f"Player - Score: {player_value}")

#deal cards
suits = ['hearts', 'diamonds', 'clubs', 'spades']
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

deck = [f'{card}_of_{suit}' for card in cards for suit in suits]

#card values
card_values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'jack':10, 'queen':10, 'king':10, 'ace':11}

dealer = []
player = []

player_card_images = []
dealer_card_images = []

dealer_value = 0
player_value = 0

#calculate hand value
def hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card.split('_')[0] == 'ace':
            aces += 1
        value += card_values[card.split('_')[0]]
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def reset():
    global deck, dealer, player, player_card_images, dealer_card_images, dealer_value, player_value
    deck = [f'{card}_of_{suit}' for card in cards for suit in suits]
    dealer.clear()
    player.clear()
    player_card_images.clear()
    dealer_card_images.clear()
    dealer_value = 0
    player_value = 0
    for widget in dealer_frame.winfo_children():
        widget.destroy()
    for widget in player_frame.winfo_children():
        widget.destroy()
    results_label.config(text="")
    if 'redeal_button' in globals():
        redeal_button.destroy()

    update_scores()
    

def deal():
    reset()
    for i in range(2):
        card = random.choice(deck)
        dealer.append(card)
        deck.remove(card)
        global dealer_image
        dealer_image = resize_image(f'cards/{card}.png')
        dealer_card_images.append(dealer_image)

        card = random.choice(deck)
        player.append(card)
        deck.remove(card)
        global player_image
        player_image = resize_image(f'cards/{card}.png')
        player_card_images.append(player_image)
        player_label = Label(player_frame, image=player_image, bg="green")
        player_label.pack(side=LEFT, padx=5)

    dealer_label = Label(dealer_frame, image=dealer_card_images[0], bg="green")
    dealer_label.pack(side=LEFT, padx=5)
    global hidden   
    hidden = resize_image(f'cards/card_back.png')
    global hidden_label
    hidden_label = Label(dealer_frame, image=hidden, bg="green")
    hidden_label.pack(side=LEFT, padx=5)

    hit_button = Button(button_frame, text="Hit", command=hit, font=("Helvetica", 20), bg="white")
    hit_button.grid(row=0, column=1, padx=10)

    stand_button = Button(button_frame, text="Stand", command=stand, font=("Helvetica", 20), bg="white")
    stand_button.grid(row=0, column=2, padx=10)
    deal_button.destroy()

    global dealer_value, player_value
    dealer_value = hand_value(dealer)
    player_value = hand_value(player)
    update_scores()

def hit():
    card = random.choice(deck)
    player.append(card)
    deck.remove(card)
    card_image = resize_image(f'cards/{card}.png')
    player_card_images.append(card_image) 
    new_label = Label(player_frame, image=card_image, bg="green")
    new_label.pack(side=LEFT, padx=5)
    global player_value
    player_value = hand_value(player)
    update_scores()
    if hand_value(player) > 21:
        results_label.config(text="Player busts! Dealer wins!")
        destroy_game_buttons()
        global redeal_button
        redeal_button = Button(button_frame, text="Re-deal", command=deal, font=("Helvetica", 20), bg="white")
        redeal_button.grid(pady=10)
        
    

#have dealer play
def stand():
    hidden_label.destroy()
    label = Label(dealer_frame, image=dealer_card_images[1], bg="green")
    label.pack(side=LEFT, padx=5)
    while hand_value(dealer) < 17:
        card = random.choice(deck)
        dealer.append(card)
        deck.remove(card)
        card_image = resize_image(f'cards/{card}.png')
        dealer_card_images.append(card_image) 
        new_label = Label(dealer_frame, image=card_image, bg="green")
        new_label.pack(side=LEFT, padx=5)
    global dealer_value, player_value
    dealer_value = hand_value(dealer)
    player_value = hand_value(player)
    update_scores()
    if player_value > 21:
        results_label.config(text="Player busts! Dealer wins!")
    elif dealer_value > 21:
        results_label.config(text="Dealer busts! Player wins!")
    elif player_value > dealer_value:
        results_label.config(text="Player wins!")
    elif dealer_value > player_value:
        results_label.config(text="Dealer wins!")
    else:
        results_label.config(text="Push!")

    destroy_game_buttons()
    global redeal_button
    redeal_button = Button(button_frame, text="Re-deal", command=deal, font=("Helvetica", 20), bg="white")
    redeal_button.grid(pady=10)

def destroy_game_buttons():
    """Disable Hit and Stand buttons after the game ends."""
    for widget in button_frame.winfo_children():
        widget.destroy()

#game frame
my_frame = Frame(root,bg="green")
my_frame.pack(pady=20)

#creation of frames for cards
dealer_frame = LabelFrame(my_frame, text=f"Dealer - Score: {dealer_value if len(dealer) > 2 else '?'}", bd=0, bg="green")
dealer_frame.grid(row=0, column=0, padx=20,ipadx=20)
player_frame = LabelFrame(my_frame, text = f"Player - Score: {player_value}", bd=0, bg="green")
player_frame.grid(row=0, column=1, ipadx=20)

# Results label
results_label = Label(root, text="", font=("Helvetica", 20), bg="green", fg="white")
results_label.pack(pady=20)

# Buttons
button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

deal_button = Button(button_frame, text="Deal", command=deal, font=("Helvetica", 20), bg="white")
deal_button.grid(row=0, column=0, padx=10)




root.mainloop()