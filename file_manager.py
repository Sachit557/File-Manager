# CustomTkinter File Manager ( some features from tkinter also utilised like filedialong simpledialog and messagebox)
import os
import sys
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# frontend looks ( colour and theme )
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Window width and height 
APP_WIDTH = 800
APP_HEIGHT = 600

app = ctk.CTk()  #the actual application 
app.title("File Manager")   #the title shown at the top of the app
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")   
app.minsize(640, 480) #minimum windows size it can be shrinked to

# starting folder = home
curr_dir = os.path.expanduser("~")


# the top bar showing your path like default starting at c-drive ( home basically)

top_bar = ctk.CTkFrame(app)
top_bar.pack(fill="x", padx=(12,12), pady=(12, 6)) # expands towards x coordinate

path_label = ctk.CTkLabel(top_bar, text=curr_dir, anchor="w") # w for west direction
path_label.pack(side="left", fill="x", expand=True, padx=(4, 8)) # expand is true so that it is able to increase in size when the window size is increased


# Major functions--
#
# change_dir(path)
# Updates the global current dir and calss refresh_view.
#
# refresh_view()
# Clears the Listbox and loads all folders/files in current dir.
#
# get_selected_item()
# Returns the currently highlighted item in the Listbox.
#
#open_selected(event=None)
#Opens a folder (navigates into it) or opens a file using OS default app.
#
#go_home()
#goes to the default ( home) dir.
#
#pick_directory()
#Opens a folder selection dialog and switches to the chosen dir.
#
#go_back(event=None)
#Moves one dir up (parent folder).
#
#new_folder()
#Creates a new folder inside the current dir.
#
#new_file()
#Creates a new file inside the current dir.
#
#delete_selected()
#Deletes the selected file (folder deletion doesnt work yet).
#
#rename_selected()
#Renames the selected file or folder.


def change_dir(path):
    """change current folder"""
    global curr_dir
    if os.path.isdir(path):
        curr_dir = os.path.abspath(path)
        refresh_view()


# drive selector (only on windows)
if sys.platform.startswith("win"):  # windows device check
    Drives = ["C:", "D:", "E:", "F:"]  # drives
    drive_var = tk.StringVar(value=Drives[0])  # referring to c drive

    def drive_select(choice):
        drive_path = choice + "\\"
        if os.path.exists(drive_path):
            change_dir(drive_path)
        else:
            messagebox.showwarning("Drive is missing", drive_path + " is not available.")

    drive_selector = ctk.CTkOptionMenu(  # it is the drop down type menu .. the options are listed in a drop down menu
        top_bar,
        values=Drives,
        variable=drive_var,
        command=drive_select #callback here it calls the drive_select function after getting the drive from the user at default c d e and f drive
    )
    drive_selector.pack(side="right", padx=(8, 4))
else:
    drive_selector = ctk.CTkLabel(top_bar, text=" macOS/Linux ")    #if not windows than mac or linux
    drive_selector.pack(side="right", padx=(8, 4))


# File list in the middle

main_area = ctk.CTkFrame(app)
main_area.pack(fill="both", expand=True, padx=12, pady=6) #both reffering to x and y padding is like gap from both sides of screen

list_frame = tk.Frame(main_area)
list_frame.pack(fill="both", expand=True)

list_scroll = tk.Scrollbar(list_frame)
list_scroll.pack(side="right", fill="y")

file_list = tk.Listbox(
    list_frame,
    yscrollcommand=list_scroll.set, 
    bg="#1e1e1e",                   #background colour of listbox
    fg="white",                       # text colour 
    selectbackground="#2b6cb0",     # background colour used when an item is selected ( blue in our case)
    selectforeground="white",         # text colour when selected
    activestyle="none",
    highlightthickness=0,
    borderwidth=0
)
file_list.pack(fill="both", expand=True)
list_scroll.config(command=file_list.yview)


#functions

def refresh_view():
    """show folders and files in listbox"""
    file_list.delete(0, tk.END) # removes all items from 0 to the end
    path_label.configure(text=curr_dir) # updates the path label ( directory in our case)

    try:
        entries = os.listdir(curr_dir) #it will list down folders from curr dir
    except PermissionError:
        entries = []                    # some cases folders might not be accessable

    entries = sorted(entries, key=str.lower) #alphabetically sorted

    # folders first in the list
    for name in entries:
        full_path = os.path.join(curr_dir, name) # technically we can concatenate but the thing is '\' works for windows while linux and mac require '/'
        if os.path.isdir(full_path):
            file_list.insert(tk.END, "[Folder] " + name) 

    # files next in the list 
    for name in entries:
        full_path = os.path.join(curr_dir, name)  # technically we can concatenate but the thing is '\' works for windows while linux and mac require '/'
        if os.path.isfile(full_path):
            file_list.insert(tk.END, name)
    # both files and folder are sorted from names as done above

def get_selected_item():
    """get selected item text"""
    selected = file_list.curselection()
    if not selected:
        return None
    return file_list.get(selected[0])


def open_selected(event=None):   #usually not needed but using tkinter it can be called with either some event or without an event
    """open folder or file"""
    picked = get_selected_item()
    if not picked:
        return

    # open folder
    if picked.startswith("[Folder] "):
        folder_name = picked.replace("[Folder] ", "") # we had [Folder] prefix , removing it for internal processing
        new_path = os.path.join(curr_dir, folder_name) 
        change_dir(new_path)
        return

    # open file
    file_path = os.path.join(curr_dir, picked)

    if sys.platform.startswith("win"):
        os.startfile(file_path)                 # windows specific
    elif sys.platform == "darwin":                  # macOS specific
        subprocess.run(["open", file_path])
    else:                                        # Linux specific
        subprocess.run(["xdg-open", file_path]) 


def go_home():
    """go to home folder"""
    home = os.path.expanduser("~")           # goes to the home folder ( mostly c/users/<user_name> for windows users)
    change_dir(home)


def pick_directory():
    """choose folder using dialog"""
    chosen = filedialog.askdirectory(initialdir=curr_dir)  # windows popup for choosing dir 
    if chosen:
        change_dir(chosen)


def go_back(event=None):
    """go to parent folder"""
    global curr_dir                             # goes to previous folder
    parent = os.path.dirname(curr_dir)
    if parent != curr_dir:
        change_dir(parent)              


def new_folder():
    """make new folder"""
    name = simpledialog.askstring("New Folder", "Folder name:") #windows based popup
    if name:
        new_path = os.path.join(curr_dir, name)
        os.mkdir(new_path)
        refresh_view()


def new_file():
    """make new file"""
    name = simpledialog.askstring("New File", "File name:")  #windows based popup
    if name:
        new_path = os.path.join(curr_dir, name)
        f = open(new_path, "x")                              # "x" means it will only create file if it does exist 
        f.close()                                            # closing the file ( it was opened just to be created)
        refresh_view()


def delete_selected():
    """delete only files, not folders"""
    picked = get_selected_item()
    if not picked:
        return

    name = picked.replace("[Folder] ", "")
    full_path = os.path.join(curr_dir, name)

    if os.path.isdir(full_path):                                            # cant delete folder cause os.rmdir can cause errors if files inside the folder
        messagebox.showinfo("Blocked", "Folder deletion disabled.")
        return

    answer = messagebox.askyesno("Delete?", "Delete file: " + name + " ?")  # windows based popup
    if answer:
        os.remove(full_path)
        refresh_view()


def rename_selected():
    """rename file or folder"""
    picked = get_selected_item()
    if not picked:
        return

    old_name = picked.replace("[Folder] ", "")
    new_name = simpledialog.askstring("Rename", "New name:", initialvalue=old_name)

    if new_name:
        old_path = os.path.join(curr_dir, old_name)
        new_path = os.path.join(curr_dir, new_name)
        os.rename(old_path, new_path)
        refresh_view()


# Control paenls at the bottom

control_bar = ctk.CTkFrame(app)
control_bar.pack(fill="x", padx=12, pady=(6, 12))

home_btn = ctk.CTkButton(control_bar, text="Home", width=100, command=go_home)
home_btn.pack(side="left", padx=6)

choose_btn = ctk.CTkButton(control_bar, text="Choose Folder", width=120, command=pick_directory)
choose_btn.pack(side="left", padx=6)

open_btn = ctk.CTkButton(control_bar, text="Open / Enter", width=120, command=open_selected)
open_btn.pack(side="left", padx=6)

back_btn = ctk.CTkButton(control_bar, text="Back", width=80, command=go_back)
back_btn.pack(side="left", padx=6)

new_folder_btn = ctk.CTkButton(control_bar, text="New Folder", width=120, command=new_folder)
new_folder_btn.pack(side="left", padx=6)

new_file_btn = ctk.CTkButton(control_bar, text="New File", width=100, command=new_file)
new_file_btn.pack(side="left", padx=6)

del_btn = ctk.CTkButton(control_bar, text="Delete File", width=120, command=delete_selected)
del_btn.pack(side="left", padx=6)

rename_btn = ctk.CTkButton(control_bar, text="Rename", width=100, command=rename_selected)
rename_btn.pack(side="left", padx=6)


# key binds for keyboard and mouse

file_list.bind("<Double-Button-1>", open_selected) # button one is actually left click so double click 
app.bind("<Return>", open_selected)      # Enter button is for open
app.bind("<BackSpace>", go_back)         # Backspace is to go up

# first load
refresh_view()

# run app
app.mainloop()

# folders cannot be deleted ( causing crash when tried)