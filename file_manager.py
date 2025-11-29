# Simple CustomTkinter File Manager

import os
import sys
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# --- Appearance ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- App Window ---
APP_WIDTH = 800
APP_HEIGHT = 600

app = ctk.CTk()
app.title("File Manager - Cross Platform")
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
app.minsize(640, 480)

# starting folder = home
curr_dir = os.path.expanduser("~")

# ─────────────────────────────
# TOP BAR
# ─────────────────────────────
top_bar = ctk.CTkFrame(app)
top_bar.pack(fill="x", padx=12, pady=(12, 6))

path_label = ctk.CTkLabel(top_bar, text=curr_dir, anchor="w")
path_label.pack(side="left", fill="x", expand=True, padx=(4, 8))


def change_dir(path):
    """change current folder"""
    global curr_dir
    if os.path.isdir(path):
        curr_dir = os.path.abspath(path)
        refresh_view()


# drive selector (only on windows)
if sys.platform.startswith("win"):
    DRIVES = ["C:", "D:", "E:", "F:"]
    drive_var = tk.StringVar(value=DRIVES[0])

    def on_drive_select(choice):
        drive_path = choice + "\\"
        if os.path.exists(drive_path):
            change_dir(drive_path)
        else:
            messagebox.showwarning("Drive missing", drive_path + " not available.")

    drive_selector = ctk.CTkOptionMenu(
        top_bar,
        values=DRIVES,
        variable=drive_var,
        command=on_drive_select
    )
    drive_selector.pack(side="right", padx=(8, 4))
else:
    drive_selector = ctk.CTkLabel(top_bar, text=" macOS/Linux ")
    drive_selector.pack(side="right", padx=(8, 4))

# ─────────────────────────────
# FILE LIST AREA
# ─────────────────────────────
main_area = ctk.CTkFrame(app)
main_area.pack(fill="both", expand=True, padx=12, pady=6)

list_frame = tk.Frame(main_area)
list_frame.pack(fill="both", expand=True)

list_scroll = tk.Scrollbar(list_frame)
list_scroll.pack(side="right", fill="y")

file_list = tk.Listbox(
    list_frame,
    yscrollcommand=list_scroll.set,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#2b6cb0",
    selectforeground="white",
    activestyle="none",
    highlightthickness=0,
    borderwidth=0
)
file_list.pack(fill="both", expand=True)
list_scroll.config(command=file_list.yview)


# ─────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────
def refresh_view():
    """show folders and files in listbox"""
    file_list.delete(0, tk.END)
    path_label.configure(text=curr_dir)

    try:
        entries = os.listdir(curr_dir)
    except PermissionError:
        entries = []

    entries = sorted(entries, key=str.lower)

    # folders first
    for name in entries:
        full_path = os.path.join(curr_dir, name)
        if os.path.isdir(full_path):
            file_list.insert(tk.END, "[Folder] " + name)

    # files next
    for name in entries:
        full_path = os.path.join(curr_dir, name)
        if os.path.isfile(full_path):
            file_list.insert(tk.END, name)


def get_selected_item():
    """get selected item text"""
    sel = file_list.curselection()
    if not sel:
        return None
    return file_list.get(sel[0])


def open_selected(event=None):
    """open folder or file"""
    picked = get_selected_item()
    if not picked:
        return

    # open folder
    if picked.startswith("[Folder] "):
        folder_name = picked.replace("[Folder] ", "")
        new_path = os.path.join(curr_dir, folder_name)
        change_dir(new_path)
        return

    # open file
    file_path = os.path.join(curr_dir, picked)

    if sys.platform.startswith("win"):
        os.startfile(file_path)
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", file_path])
    else:  # Linux
        subprocess.run(["xdg-open", file_path])


def go_home():
    """go to home folder"""
    home = os.path.expanduser("~")
    change_dir(home)


def pick_directory():
    """choose folder using dialog"""
    chosen = filedialog.askdirectory(initialdir=curr_dir)
    if chosen:
        change_dir(chosen)


def go_back(event=None):
    """go to parent folder"""
    global curr_dir
    parent = os.path.dirname(curr_dir)
    if parent != curr_dir:
        change_dir(parent)


def new_folder():
    """make new folder"""
    name = simpledialog.askstring("New Folder", "Folder name:")
    if name:
        new_path = os.path.join(curr_dir, name)
        os.mkdir(new_path)
        refresh_view()


def new_file():
    """make new file"""
    name = simpledialog.askstring("New File", "File name:")
    if name:
        new_path = os.path.join(curr_dir, name)
        f = open(new_path, "x")
        f.close()
        refresh_view()


def delete_selected():
    """delete only files, not folders"""
    picked = get_selected_item()
    if not picked:
        return

    name = picked.replace("[Folder] ", "")
    full_path = os.path.join(curr_dir, name)

    if os.path.isdir(full_path):
        messagebox.showinfo("Blocked", "Folder deletion disabled.")
        return

    answer = messagebox.askyesno("Delete?", "Delete file: " + name + " ?")
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


# ─────────────────────────────
# CONTROL PANEL BUTTONS
# ─────────────────────────────
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

# ─────────────────────────────
# KEY BINDINGS
# ─────────────────────────────
file_list.bind("<Double-Button-1>", open_selected)
app.bind("<Return>", open_selected)      # Enter → open
app.bind("<BackSpace>", go_back)         # Backspace → go up

# first load
refresh_view()

# run app
app.mainloop()
