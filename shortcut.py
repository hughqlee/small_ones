import tkinter as tk

from os import remove, rename
from glob import glob
from PIL import ImageTk, Image

images = glob('*.JPG') # 확장자명 유의
unclassified_images = filter(lambda image: image, images) # iter/generator 형식 필요. for next()
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
    remove(current)
    next_img()

def move(arg):
    global current
    rename(current, arg+"/"+current)
    next_img()

def key(event):
    '''
    지우거나 폴더를 이동시키는 기능
    ex.) d를 누르면 삭제, s를 누르면 'side' 이름의 하위 폴더로 이동
    
    elif repr(event.char) == "'단축키'":
        move('폴더명(클래스명)')
    '''
    print('pressed', repr(event.char))
    if repr(event.char) == "'d'":
        delete()
    elif repr(event.char) == "'s'":
        move('side')
    elif repr(event.char) == "'c'":
        move('cut')
    elif repr(event.char) == "'f'":
        move('front')
    elif repr(event.char) == "'n'":
        move('normal')
    elif repr(event.char) == "'m'":
        move('multiple')
    elif repr(event.char) == "'b'":
        move('back')

if __name__ == "__main__":

    root = tk.Tk()

    img_label = tk.Label(root)
    img_label.pack()
    root.bind("<Key>", key)

    next_img() # load first image

    root.mainloop()
