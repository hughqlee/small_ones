import os
import tkinter as tk

from os import rename
from glob import glob
from PIL import ImageTk, Image

images = glob('*.jpg')
unclassified_images = filter(lambda image: image, images)
current = None

def next_img():
    global current, unclassified_images
    try:
        current = next(unclassified_images)
    except StopIteration:
        root.quit()
    print(current)
    pil_img = Image.open(current)
    width, height = pil_img.size
    max_height = 1000
    if height > max_height:
        resize_factor = max_height / height
        pil_img = pil_img.resize((int(width*resize_factor), int(height*resize_factor)), resample=Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(pil_img)
    img_label.img = img_tk
    img_label.config(image=img_label.img)
    root.title(current)

def delete():
    global current
    os.remove(current)
    next_img()

def move(arg):
    global current
    rename(current, arg+"/"+current)
    next_img()

def key(event):
    print('pressed', repr(event.char))
    if repr(event.char) == "'d'":
        delete()
    elif repr(event.char) == "'a'":
        move('daisy')
    elif repr(event.char) == "'n'":
        move('dandelion')
    elif repr(event.char) == "'r'":
        move('roses')
    elif repr(event.char) == "'s'":
        move('sunflowers')
    elif repr(event.char) == "'t'":
        move('tulips')

if __name__ == "__main__":

    root = tk.Tk()

    img_label = tk.Label(root)
    img_label.pack()
    root.bind("<Key>", key)

    next_img() # load first image

    root.mainloop()