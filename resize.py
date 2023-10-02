from tkinter import *
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ------ Constants ------
PRIMARY_COLOR = "#3E3E3E"
SECONDARY_COLOR = "#405559"
TERTIARY_COLOR = "#5C527F"
STARTING_W = 625
STARTING_H = 625
LABEL_FONT = ("Optima", 10, 'italic')

# ------ Window and frame attributes -------
dynamic_w = 439
dynamic_h = 511
global direction

window = Tk()
window.title("Image Mover")
window.config(bg=SECONDARY_COLOR, padx=12, pady=12)
window.minsize(width=STARTING_W, height=STARTING_H)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=0)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, minsize=dynamic_h)
window.rowconfigure(2, weight=1)

frame = Frame(width=dynamic_w, height=dynamic_h, highlightthickness=0, bg=PRIMARY_COLOR, borderwidth=4, relief=SUNKEN)
frame.grid(column=0, row=1, sticky="WENS")
frame.propagate(False)

r_frame = Frame(bg=SECONDARY_COLOR)
r_frame.grid(column=1, row=0, rowspan=3, sticky="WENS")
r_frame.rowconfigure(0, weight=1)
r_frame.rowconfigure(1, weight=1)
r_frame.rowconfigure(2, weight=1)
r_frame.rowconfigure(3, weight=0)

button_frame = Frame(r_frame, bg=SECONDARY_COLOR)
button_frame.grid(row=3, sticky="WENS")
spacer = Label(button_frame)
spacer.config(background=SECONDARY_COLOR)
spacer.grid(column=0, padx=(8, 0))
r_frame.columnconfigure(0, weight=1)
r_frame.columnconfigure(4, weight=1)
r_frame.rowconfigure(0, weight=1)
r_frame.rowconfigure(6, weight=1)

ins_label = Label(r_frame, bg=SECONDARY_COLOR, font=LABEL_FONT, justify=LEFT, fg="#EDEDED",
                  text="\n- Click arrow to select "
                       "\n  destination\n"
                       "- Press arrow key to move\n"
                       "- Space to skip image\n"
                       "- Backspace to undo move")
ins_label.grid(row=4, sticky="WENS")


# Sets new image's size appropriately, and returns scale for use in other resizing functions
def set_image(image):
    image_width = image.width
    image_height = image.height
    aspect_ratio = image_width / image_height
    print(aspect_ratio)


    if image_width > image_height:
        if frame.winfo_width() > 50:
            new_iwidth = frame.winfo_width()
            print("frame", frame.winfo_width())
        else:
            new_iwidth = dynamic_w
            print("dyn", dynamic_w)
        new_iheight = new_iwidth / aspect_ratio
        new = image.resize((int(new_iwidth), int(new_iheight)))
        return new, "horizontal"
    else:
        if frame.winfo_height() > 50:
            new_iheight = frame.winfo_height()
        else:
            new_iheight = dynamic_h
        new_iwidth = new_iheight * aspect_ratio
        new = image.resize((int(new_iwidth), int(new_iheight)))
        return new, "vertical"


# ------ Image and image label attributes ------


image = resource_path("default.bmp")


def update_image(img):
    global direction, image_base, image
    image = img
    image_og = (Image.open(image))
    image_scaled, direction = set_image(image_og)

    image_base = ImageTk.PhotoImage(image_scaled)
    image_bg.config(image=image_base)


image_bg = Label(frame, bg=PRIMARY_COLOR)
image_bg.pack(fill=BOTH, expand=TRUE)

update_image(image)


# Keeps window to given aspect ratio when resizing
def enforce_aspect_ratio(event, window):

    ar = 1/1

    if event.widget == event.widget.winfo_toplevel():

        desired_width = event.width
        desired_height = int(event.width / ar)

        if desired_height == event.height and desired_width == event.width:
            return

        if desired_height > event.height:
            desired_height = event.height
            desired_width = int(event.height * ar)

        window.geometry(f"{desired_width}x{desired_height}")


        # ------ Resize function for frame and contained image ------
        global bg, resized_bg, new_bg
        bg = Image.open(image)


        # Sets new frame size
        new_fwidth, new_fheight = desired_width - 250, desired_height - 125
        frame.config(width=new_fwidth, height=new_fheight)

        # Calculates new dimensions for image
        aspect_ratio = bg.width / bg.height
        print("aspect ratio: ", aspect_ratio, "bg.width: ", bg.width, "bg.height: ", bg.height)
        if direction == "horizontal":
            new_iwidth = frame.winfo_width()
            print("frame.width: ", frame.winfo_width())
            print("frame.height: ", frame.winfo_height())
            new_iheight = new_iwidth / aspect_ratio
            print("new.height: ", new_iheight)
        elif direction == "vertical":
            new_iheight = frame.winfo_height()
            print("frame.height: ", frame.winfo_height())
            new_iwidth = new_iheight * aspect_ratio
            print("new.width: ", new_iwidth)
        else:
            new_iwidth = frame.winfo_width()
            new_iheight = frame.winfo_height()

        print(int(new_iheight), int(new_iwidth))

        if int(new_iwidth) > 0 and int(new_iheight) > 0:
            resized_bg = bg.resize((int(new_iwidth), int(new_iheight)))
            new_bg = ImageTk.PhotoImage(resized_bg)
            image_bg.config(image=new_bg)

        dynamic_w = new_fwidth + 180
        dynamic_h = new_fheight + 180

        return dynamic_w, dynamic_h



window.bind("<Configure>", lambda event, window=window: enforce_aspect_ratio(event, window))
