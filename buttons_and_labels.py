from tkinter import *
from tkinter import filedialog
import os
import shutil
from resize import  image, update_image


LABEL_FONT = ("Optima", 10, 'italic')
IMAGE_TAGS = (".jpg", ".JPG", ".png", ".PNG", ".jpeg", ".JPEG", ".bmp", ".BMP", ".gif", ".GIF", ".tiff", ".TIFF",
              ".ppm", ".PPM", ".ico", ".ICO", ".psd", ".PSD")

# ------ Some Variables ------
up_directory = None
down_directory = None
right_directory = None
left_directory = None
image_directory = None
image_list = []
undo_list = []

def move_image(directory):


    cur_img = os.path.join(image_directory, image_list[0])
    if os.path.isfile(cur_img):
        shutil.move(cur_img, os.path.join(directory, image_list[0]))
        print(image_directory)
        print(image_list[0])
        if len(undo_list) >= 100:
            undo_list.pop()
            undo_list.insert(0, [directory, image_list[0]])
        else:
            undo_list.insert(0, [directory, image_list[0]])
        image_list.pop(0)
        if image_list:
            print(image_list)
            update_image(os.path.join(image_directory, image_list[0]))
        else:
            update_image("default.bmp")



def key_action(event):
    if image_list:
        if event.keysym == "Up" and up_directory:
            move_image(up_directory)

        if event.keysym == "Down" and down_directory:
            move_image(down_directory)

        if event.keysym == "Left" and left_directory:
            move_image(left_directory)

        if event.keysym == "Right" and right_directory:
            move_image(right_directory)

        if event.keysym == "space":
            if len(undo_list) >= 100:
                undo_list.pop()
                undo_list.insert(0, [image_directory, image_list[0]])
            else:
                undo_list.insert(0, [image_directory, image_list[0]])
            image_list.pop(0)
            if image_list:
                print(image_list)
                update_image(os.path.join(image_directory, image_list[0]))
            else:
                update_image("default.bmp")

    if event.keysym == "BackSpace":
        if undo_list:
            shutil.move(os.path.join(undo_list[0][0], undo_list[0][1]), os.path.join(image_directory, undo_list[0][1]))
            image_list.insert(0, undo_list[0][1])
            update_image(os.path.join(image_directory, image_list[0]))
            undo_list.pop(0)


def list_image_files():
    global image_list, image_directory

    directory = filedialog.askdirectory()
    if directory:
        image_files = [file
                       for file in os.listdir(directory)
                       if os.path.isfile(os.path.join(directory, file)) and file.endswith(IMAGE_TAGS)]

        image_list = image_files
        image_directory = directory
        if image_files:
            image = os.path.join(directory, image_files[0])
            update_image(image)

class ArrowButton(Button):

    def __init__(self, master):
        super().__init__(master)
        self.configure(borderwidth=0, relief="flat", highlightthickness=0)
        # Need to add frame location, image, activebackground (SECONDARY COLOR) and folder_click command


class FolderLabel(Entry):

    def __init__(self, master, window):
        super().__init__(master)
        self.configure(font=LABEL_FONT, fg="#EDEDED", relief="flat", justify=CENTER,
                       disabledforeground="#EDEDED", width=7)
        # Need to add frame location, bg (SECONDARY COLOR), disabled bg (SECONDARY COLOR)
        self.bind('<Return>', self.enter)
        self.bind('<Button-1>', self.click_label)
        self.window = window

    # Upon selecting folder, creates and returns list of image file paths in that folder


    # Makes label editable and updates it upon selecting a folder and updates folder path variable
    def folder_click(self, dir_var):
        global up_directory, down_directory, left_directory, right_directory
        directory = filedialog.askdirectory()
        self.configure(state=NORMAL, relief=SUNKEN)
        self.delete(0, END)
        self.insert(0, "Label")
        if dir_var == "Up":
            up_directory = directory
        elif dir_var == "Down":
            down_directory = directory
        elif dir_var == "Left":
            left_directory = directory
        elif dir_var == "Right":
            right_directory = directory



    # Clears label entry box after "enter" key
    def enter(self, event):
        self.configure(relief=FLAT)
        self.window.focus_set()

    # Clears placeholder in Entry box when clicked and allows user to edit a label text
    def click_label(self, event):
        if self.get() == "Label":
            self.delete(0, END)
        elif self.get() != "Select":
            self.configure(relief=SUNKEN)
