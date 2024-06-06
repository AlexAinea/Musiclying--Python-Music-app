from tkinter import *
from PIL import Image, ImageTk
import hashlib
import random
from io import BytesIO
import pygame
import database
import os
from tkinter import filedialog

current_index = 0
is_paused = False
is_shuffled = False

def play():
    global playlist, current_index, is_paused
    if playlist.size() == 0:
        return
    
    if playlist.curselection():
        current_index = playlist.curselection()[0]
    
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        music_name = playlist.get(current_index)
        if music_name:
            pygame.mixer.music.load(music_name)
            pygame.mixer.music.play()

def stop():
    global is_paused
    pygame.mixer.music.stop()
    is_paused = False

def pause():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def next():
    global playlist, current_index, is_paused
    if playlist.size() == 0:
        return

    if is_shuffled:
        current_index = random.randint(0, playlist.size() - 1)
    else:
        current_index = (current_index + 1) % playlist.size()

    playlist.selection_clear(0, END)
    playlist.selection_set(current_index)
    is_paused = False
    play()

def previous():
    global playlist, current_index, is_paused
    if playlist.size() == 0:
        return

    if is_shuffled:
        current_index = random.randint(0, playlist.size() - 1)
    else:
        current_index = (current_index - 1) % playlist.size()

    playlist.selection_clear(0, END)
    playlist.selection_set(current_index)
    is_paused = False
    play()

def add_music():
    global playlist
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def toggle_shuffle():
    global is_shuffled
    is_shuffled = not is_shuffled
    shuffle_label.config(text="Shuffle: ON" if is_shuffled else "Shuffle: OFF")

def main_page(user):
    global avatar_image, playlist, current_index, is_paused, is_shuffled, shuffle_label
    auth_root.destroy()

    main_page_root = Tk()
    main_page_root.geometry("800x1000")
    main_page_root.title("Musiclying")

    pygame.mixer.init()

    user_name = user[0]
    user_binary_avatar = user[2]

    image = Image.open(BytesIO(user_binary_avatar))
    image = image.resize((50, 50))
    avatar_image = ImageTk.PhotoImage(image)

    user_details_frame = Frame(main_page_root)
    user_details_frame.pack(pady=20)

    Label(user_details_frame, image=avatar_image).pack(side=LEFT)
    Label(user_details_frame, text=f"Welcome {user_name}!").pack(side=LEFT)

    gifs = ['assets/gifs/loop.gif','assets/gifs/loop1.gif','assets/gifs/loop2.gif','assets/gifs/loop3.gif',
            'assets/gifs/loop4.gif','assets/gifs/loop5.gif','assets/gifs/loop6.gif','assets/gifs/loop7.gif','assets/gifs/loop8.gif','assets/gifs/loop9.gif']
    
    gif = random.choice(gifs)
    print(gif)

    frames = []
    ind = 0

    while True:
        try:
            frame = PhotoImage(file=gif, format=f'gif -index {ind}')
            frames.append(frame)
            ind += 1
        except TclError:
            break

    frame_count = len(frames)

    def update(ind):
        frame = frames[ind]
        ind = (ind + 1) % frame_count

        label.configure(image=frame)
        main_page_root.after(40, update, ind)

    label = Label(main_page_root, width=500, height=300)
    label.pack(pady=20, padx=20)
    main_page_root.after(0, update, 0)

    music_manipulation_frame = Frame(main_page_root)
    music_manipulation_frame.pack(pady=20)

    previous_image = Image.open("assets/images/back.png")
    previous_image = previous_image.resize((50, 50))
    previous_image = ImageTk.PhotoImage(previous_image)
    Button(music_manipulation_frame, image=previous_image, command=previous).grid(row=0, column=0)

    play_image = Image.open("assets/images/play.png")
    play_image = play_image.resize((50, 50))
    play_image = ImageTk.PhotoImage(play_image)
    Button(music_manipulation_frame, image=play_image, command=play, bg="#ffffff").grid(row=0, column=1)

    stop_image = Image.open("assets/images/stop.png")
    stop_image = stop_image.resize((50, 50))
    stop_image = ImageTk.PhotoImage(stop_image)
    Button(music_manipulation_frame, image=stop_image, command=stop).grid(row=0, column=2)

    pause_image = Image.open("assets/images/pause.png")
    pause_image = pause_image.resize((50, 50))
    pause_image = ImageTk.PhotoImage(pause_image)
    Button(music_manipulation_frame, image=pause_image, command=pause).grid(row=0, column=3)

    next_image = Image.open("assets/images/forward.png")
    next_image = next_image.resize((50, 50))
    next_image = ImageTk.PhotoImage(next_image)
    Button(music_manipulation_frame, image=next_image, command=next).grid(row=0, column=4)

    add_image = Image.open("assets/images/add-removebg-preview.png")
    add_image = add_image.resize((50, 50))
    add_image = ImageTk.PhotoImage(add_image)
    Button(music_manipulation_frame, image=add_image, command=add_music).grid(row=0, column=5)

    # Add volume slider
    volume_frame = Frame(main_page_root)
    volume_frame.pack(pady=20)
    volume_slider = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
    volume_slider.set(50)  # Set default volume to 50%
    volume_slider.pack()

    # Add shuffle label and button
    shuffle_frame = Frame(main_page_root)
    shuffle_frame.pack(pady=20)
    shuffle_label = Label(shuffle_frame, text="Shuffle: OFF")
    shuffle_label.pack(side=LEFT)
    shuffle_button = Button(shuffle_frame, text="Toggle Shuffle", command=toggle_shuffle)
    shuffle_button.pack(side=RIGHT)

    lower_frame = Frame(main_page_root)
    lower_frame.pack() 
    playlist = Listbox(lower_frame, width=100, bg='#333333', fg='grey', selectbackground='purple', cursor='hand2')
    playlist.pack()

    main_page_root.mainloop()

def handle_sign_up(inputed_user_name, inputed_password, inputed_image_path):
    hasher = hashlib.sha256()
    hasher.update(inputed_password.encode())
    inputed_password_hash = hasher.hexdigest()

    with open(inputed_image_path, 'rb') as pre_binary:
        binary = pre_binary.read()

    database.sign_up(inputed_user_name, inputed_password_hash, binary)
    print("User signed up successfully")

def handle_login(inputed_user_name, inputed_password):
    hasher = hashlib.sha256()
    hasher.update(inputed_password.encode())
    inputed_password_hash = hasher.hexdigest()

    user = database.login(inputed_user_name, inputed_password_hash)
    if user:
        print("Login successful")
        main_page(user)
    else:
        print("Invalid credentials")

def create_sign_up_form():
    global current_form_frame
    if current_form_frame:
        current_form_frame.destroy()

    current_form_frame = Frame(auth_root)
    current_form_frame.pack(pady=20)

    Label(current_form_frame, text="User Name:").grid(row=1, column=0, padx=20, pady=20)
    user_name_entry = Entry(current_form_frame, width=30)
    user_name_entry.grid(row=1, column=1, padx=20, pady=20)

    Label(current_form_frame, text="Password:").grid(row=2, column=0, padx=20, pady=20)
    password_entry = Entry(current_form_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, padx=20, pady=20)

    Label(current_form_frame, text="Enter image path:").grid(row=3, column=0, padx=20, pady=20)
    image_path_entry = Entry(current_form_frame, width=30)
    image_path_entry.grid(row=3, column=1, padx=20, pady=20)

    Button(current_form_frame, text="SIGN UP", command=lambda: handle_sign_up(user_name_entry.get(), password_entry.get(), image_path_entry.get())).grid(row=4, column=0, columnspan=2, padx=20, pady=20)

def create_login_form():
    global current_form_frame
    if current_form_frame:
        current_form_frame.destroy()

    current_form_frame = Frame(auth_root)
    current_form_frame.pack(pady=20)

    Label(current_form_frame, text="User Name:").grid(row=1, column=0, padx=20, pady=20)
    user_name_entry = Entry(current_form_frame, width=30)
    user_name_entry.grid(row=1, column=1, padx=20, pady=20)

    Label(current_form_frame, text="Password:").grid(row=2, column=0, padx=20, pady=20)
    password_entry = Entry(current_form_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, padx=20, pady=20)

    Button(current_form_frame, text="LOG IN", command=lambda: handle_login(user_name_entry.get(), password_entry.get())).grid(row=3, column=0, columnspan=2, padx=20, pady=20)

auth_root = Tk()
auth_root.geometry("")
auth_root.title("Authentication")

auth_frame = Frame(auth_root)
auth_frame.pack(pady=50)

current_form_frame = None

create_sign_up_form()

Button(auth_frame, text="Switch to Sign Up", command=create_sign_up_form).pack(pady=10)
Button(auth_frame, text="Switch to Login", command=create_login_form).pack(pady=10)

auth_root.mainloop()
