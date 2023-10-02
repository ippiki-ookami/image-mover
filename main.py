from resize import *
from buttons_and_labels import ArrowButton, FolderLabel, list_image_files, key_action
from resize import window
from resize import resource_path

# ------ Constants ------
PRIMARY_COLOR = "#3E3E3E"
SECONDARY_COLOR = "#405559"
TERTIARY_COLOR = "#5C527F"





# ------ Buttons and Labels placement ------
up_image = PhotoImage(file=resource_path("up_arrow1.png"))
down_image = PhotoImage(file=resource_path("down_arrow1.png"))
right_image = PhotoImage(file=resource_path("right_arrow1.png"))
left_image = PhotoImage(file=resource_path("left_arrow1.png"))



# ------ Image Folder Button ------
img_fldr_button = Button(r_frame)
img_fldr_button.configure(text="Select Image Folder", activebackground=SECONDARY_COLOR,
                    command=list_image_files)
img_fldr_button.grid(row=1, column=0, padx=(18, 0))

# ------ Up Folder Button ------
up_button = ArrowButton(button_frame)
up_button.configure(image=up_image, activebackground=SECONDARY_COLOR,
                    command=lambda: up_label.folder_click("Up"))
up_button.grid(column=2, row=2, rowspan=2)
up_label = FolderLabel(button_frame, window)
up_label.configure(bg=SECONDARY_COLOR, disabledbackground=SECONDARY_COLOR)
up_label.grid(column=2, row=1)
up_label.insert(0, "Select")
up_label.configure(state=DISABLED)

# ------ Down Folder Button ------
down_button = ArrowButton(button_frame)
down_button.configure(image=down_image, activebackground=SECONDARY_COLOR,
                      command=lambda: down_label.folder_click("Down"))
down_button.grid(column=2, row=4)
down_label = FolderLabel(button_frame, window)
down_label.configure(bg=SECONDARY_COLOR, disabledbackground=SECONDARY_COLOR)
down_label.grid(column=2, row=5)
down_label.insert(0, "Select")
down_label.configure(state=DISABLED)

# ------ Right Folder Button ------
right_button = ArrowButton(button_frame)
right_button.configure(image=right_image, activebackground=SECONDARY_COLOR,
                       command=lambda: right_label.folder_click("Right"))
right_button.grid(column=3, row=4)
right_label = FolderLabel(button_frame, window)
right_label.configure(bg=SECONDARY_COLOR, disabledbackground=SECONDARY_COLOR)
right_label.grid(column=3, row=3)
right_label.insert(0, "Select")
right_label.configure(state=DISABLED)

# ------ Left Folder Button ------
left_button = ArrowButton(button_frame)
left_button.configure(image=left_image, activebackground=SECONDARY_COLOR,
                       command=lambda: left_label.folder_click("Left"))
left_button.grid(column=1, row=4)
left_label = FolderLabel(button_frame, window)
left_label.configure(bg=SECONDARY_COLOR, disabledbackground=SECONDARY_COLOR)
left_label.grid(column=1, row=3)
left_label.insert(0, "Select")
left_label.configure(state=DISABLED)



window.bind('<KeyRelease-Up>', key_action)
window.bind('<KeyRelease-Down>', key_action)
window.bind('<KeyRelease-Left>', key_action)
window.bind('<KeyRelease-Right>', key_action)

window.bind('<KeyRelease-BackSpace>', key_action)
window.bind('<KeyRelease-space>', key_action)


window.mainloop()
