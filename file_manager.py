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
root_dir = os.path.expanduser("~")

# ─────────────────────────────
# TOP BAR
# ─────────────────────────────
top_frame = ctk.CTkFrame(app)
top_frame.pack(fill="x", padx=12, pady=(12, 6))

dir_label = ctk.CTkLabel(top_frame, text=root_dir, anchor="w")
dir_label.pack(side="left", fill="x", expand=True, padx=(4, 8))


def change_dir(path):
    """change current folder"""
    global root_dir
    if os.path.isdir(path):
        root_dir = os.path.abspath(path)
        update_view()


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

    drive_menu = ctk.CTkOptionMenu(
        top_frame,
        values=DRIVES,
        variable=drive_var,
        command=on_drive_select
    )
    drive_menu.pack(side="right", padx=(8, 4))
else:
    drive_menu = ctk.CTkLabel(top_frame, text=" macOS/Linux ")
    drive_menu.pack(side="right", padx=(8, 4))

# ─────────────────────────────
# FILE LIST AREA
# ─────────────────────────────
ui_frame = ctk.CTkFrame(app)
ui_frame.pack(fill="both", expand=True, padx=12, pady=6)

listbox_frame = tk.Frame(ui_frame)
listbox_frame.pack(fill="both", expand=True)

scroll_bar = tk.Scrollbar(listbox_frame)
scroll_bar.pack(side="right", fill="y")

item_list = tk.Listbox(
    listbox_frame,
    yscrollcommand=scroll_bar.set,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#2b6cb0",
    selectforeground="white",
    activestyle="none",
    highlightthickness=0,
    borderwidth=0
)
item_list.pack(fill="both", expand=True)
scroll_bar.config(command=item_list.yview)


# ─────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────
def update_view():
    """show folders and files in listbox"""
    item_list.delete(0, tk.END)
    dir_label.configure(text=root_dir)

    entries = os.listdir(root_dir)
    entries = sorted(entries, key=str.lower)

    # folders first
    for name in entries:
        full_path = os.path.join(root_dir, name)
        if os.path.isdir(full_path):
            item_list.insert(tk.END, "[Folder] " + name)

    # files next
    for name in entries:
        full_path = os.path.join(root_dir, name)
        if os.path.isfile(full_path):
            item_list.insert(tk.END, name)


def get_selected():
    """get selected item text"""
    sel = item_list.curselection()
    if not sel:
        return None
    return item_list.get(sel[0])


def open_item(event=None):
    """open folder or file"""
    picked = get_selected()
    if not picked:
        return

    # open folder
    if picked.startswith("[Folder] "):
        folder_name = picked.replace("[Folder] ", "")
        new_path = os.path.join(root_dir, folder_name)
        change_dir(new_path)
        return

    # open file
    file_path = os.path.join(root_dir, picked)

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


def browse_dir():
    """choose folder using dialog"""
    chosen = filedialog.askdirectory(initialdir=root_dir)
    if chosen:
        change_dir(chosen)


def go_up(event=None):
    """go to parent folder"""
    global root_dir
    parent = os.path.dirname(root_dir)
    if parent != root_dir:
        change_dir(parent)


def create_folder():
    """make new folder"""
    name = simpledialog.askstring("New Folder", "Folder name:")
    if name:
        new_path = os.path.join(root_dir, name)
        os.mkdir(new_path)
        update_view()


def create_file():
    """make new file"""
    name = simpledialog.askstring("New File", "File name:")
    if name:
        new_path = os.path.join(root_dir, name)
        # "x" = create new file, error if exists (we are ignoring error handling as requested)
        f = open(new_path, "x")
        f.close()
        update_view()


def delete_file():
    """delete only files, not folders"""
    picked = get_selected()
    if not picked:
        return

    # remove [Folder] if present
    name = picked.replace("[Folder] ", "")
    full_path = os.path.join(root_dir, name)

    # block folder delete
    if os.path.isdir(full_path):
        messagebox.showinfo("Blocked", "Folder deletion disabled.")
        return

    answer = messagebox.askyesno("Delete?", "Delete file: " + name + " ?")
    if answer:
        os.remove(full_path)
        update_view()


def rename_entry():
    """rename file or folder"""
    picked = get_selected()
    if not picked:
        return

    old_name = picked.replace("[Folder] ", "")
    new_name = simpledialog.askstring("Rename", "New name:", initialvalue=old_name)

    if new_name:
        old_path = os.path.join(root_dir, old_name)
        new_path = os.path.join(root_dir, new_name)
        os.rename(old_path, new_path)
        update_view()


# ─────────────────────────────
# CONTROL PANEL BUTTONS
# ─────────────────────────────
controls = ctk.CTkFrame(app)
controls.pack(fill="x", padx=12, pady=(6, 12))

home_btn = ctk.CTkButton(controls, text="Home", width=100, command=go_home)
home_btn.pack(side="left", padx=6)

choose_btn = ctk.CTkButton(controls, text="Choose Folder", width=120, command=browse_dir)
choose_btn.pack(side="left", padx=6)

open_btn = ctk.CTkButton(controls, text="Open / Enter", width=120, command=open_item)
open_btn.pack(side="left", padx=6)

back_btn = ctk.CTkButton(controls, text="Back", width=80, command=go_up)
back_btn.pack(side="left", padx=6)

new_folder_btn = ctk.CTkButton(controls, text="New Folder", width=120, command=create_folder)
new_folder_btn.pack(side="left", padx=6)

new_file_btn = ctk.CTkButton(controls, text="New File", width=100, command=create_file)
new_file_btn.pack(side="left", padx=6)

del_btn = ctk.CTkButton(controls, text="Delete File", width=120, command=delete_file)
del_btn.pack(side="left", padx=6)

rename_btn = ctk.CTkButton(controls, text="Rename", width=100, command=rename_entry)
rename_btn.pack(side="left", padx=6)

# ─────────────────────────────
# KEY BINDINGS
# ─────────────────────────────
item_list.bind("<Double-Button-1>", open_item)
app.bind("<Return>", open_item)      # Enter → open
app.bind("<BackSpace>", go_up)       # Backspace → go up

# first load
update_view()

# run app
app.mainloop()