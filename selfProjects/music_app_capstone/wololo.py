from tkinter import *
import os

root = Tk()
root.geometry("800x600")
root.title("Practice")

frames = []
ind = 0

while True:
    try:
        frame = PhotoImage(file="loop.gif", format='gif -index %i' % ind)
        frames.append(frame)
        ind += 1
    except TclError:
        break

frame_count = len(frames)

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frame_count:
        ind = 0

    label.configure(image=frame)
    root.after(5, update, ind)  # Decrease delay to 20 milliseconds for faster animation

label = Label(root)
label.pack()
root.after(0, update, 0)

root.mainloop()
