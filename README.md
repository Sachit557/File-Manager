# **File Manager**

A **cross-platform, GUI-based file manager written in Python** using **CustomTkinter**.  
The program allows **browsing directories**, **opening files**, **creating and renaming files and folders**, and **navigating drives (Windows only)**.  
It features a **dark theme with blue accents** and a **clean, intuitive interface**.

---

## **Features**

### **File Operations**
- **Open / Enter** – Open files with the system’s default application or enter folders to navigate deeper.  
- **Create Folder** – Create new folders in the current directory.  
- **Create File** – Create new empty files.  
- **Rename** – Rename files or folders.  
- **Delete File** – Delete files only (**folder deletion blocked for safety**).  

### **Navigation**
- **Home** – Return to the user’s home directory.  
- **Back** – Go to the parent folder.  
- **Choose Folder** – Browse and select a folder using a dialog.  
- **Drive Selector (Windows)** – Quickly switch between **C**, **D**, **E**, **F** drives.  
- **Cross-platform** – Works on **Windows**, **macOS**, and **Linux**. On macOS/Linux, drive selector is replaced with a label.

---

## **File / Folder Display**

| **Type**   | **Description** |
|------------|-----------------|
| **Folder** | Displayed with `[Folder]` prefix and distinguished in the list. |
| **File**   | Displayed normally with ability to open using double-click. |

---

## **How to Use**

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/Sachit557/File-Manager.git
   cd File-Manager
2. **Install dependencies**:
   pip install customtkinter
3. **Run the program**:
   python fm_simple.py
4. **Use the interface buttons and top bar to navigate, open files, and manage folders/files.**

Input Validation / Safety

Folder deletion is disabled to prevent accidental data loss.

File/folder names must be valid for the operating system.

Only existing files/folders can be renamed or opened.

Screenshots

(Add sample screenshots of the file manager here for better visual understanding)

Future Improvements

Add file preview (text/images) inside the GUI.

Implement multi-file selection and batch operations.

Add search functionality within folders.

Add theme customization (light/dark mode toggle).

Language and Tools

Written in Python 3.8+ using:

import os
import sys
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


CustomTkinter for GUI

Standard Python libraries: os, sys, subprocess, tkinter

License

Open-source project created for educational purposes and demonstration of a cross-platform GUI-based file manager in Python.
