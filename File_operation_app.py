import os
import pathlib
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox,PhotoImage
import threading
from PIL import Image, ImageTk

def perform_action(source_folder, destination_folder, selected_extension, action_type, progress_var, total_files):
    progress_step = 100 / total_files
    progress_value = 0

    def update_progress():
        nonlocal progress_value
        progress_var.set(progress_value)
        progress_value += progress_step
        app.update_idletasks()

    try:
        for item in source_folder.rglob(f"*.{selected_extension}"):
            if item.is_file():
                dest_file = destination_folder / item.name
                if dest_file.exists():
                    dest_file = destination_folder / f"{item.stem}_{item.suffix}"
                if action_type == "Copy":
                    shutil.copy(item, dest_file)
                elif action_type == "Move":
                    shutil.move(item, dest_file)
                print(f"{action_type} {item} to {dest_file}")
                update_progress()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_button(entry_var):
    folder_selected = filedialog.askdirectory()
    entry_var.set(folder_selected)

def update_extensions(selected_file_type):
    if selected_file_type == "Text":
        return ["txt", "rtf", "docx", "csv", "pdf", "wps", "wpd", "msg"]
    elif selected_file_type == "Audio":
        return ["mp3", "wma", "snd", "wav", "ra", "au", "aac"]
    elif selected_file_type == "Program file":
        return ["c", "cpp", "java", "py", "js", "ts", "cs", "swift", "dta", "pl", "sh", "bat", "com", "exe", "apk"]
    elif selected_file_type == "Compressed":
        return ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "hqx", "arj", "arc", "sit", "z", "iso", "img", "raw"]
    elif selected_file_type == "Video":
        return ["mp4", "3gp", "avi", "mpg", "mov", "wmv","mkv"]
    elif selected_file_type == "Image":
        return ["png", "jpg", "jpeg", "bmp", "gif"]
    else:
        return []

def update_extension_options(event):
    selected_file_type = file_type_combobox.get()
    extensions = update_extensions(selected_file_type)
    extension_combobox['values'] = extensions
    extension_combobox.current(0)

def perform_action_button():
    source_folder = pathlib.Path(source_entry.get())
    destination_folder = pathlib.Path(destination_entry.get())
    selected_extension = extension_combobox.get()
    selected_action = action_combobox.get()

    if not source_folder.exists() or not destination_folder.exists():
        messagebox.showerror("Error", "Source or destination folder does not exist.")
        return

    total_files = len(list(source_folder.rglob(f"*.{selected_extension}")))
    # messagebox.showinfo("Total Files", f"Total number of files to be {selected_action.lower()}: {total_files}")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(app, variable=progress_var, length=700, mode="determinate")
    progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    thread = threading.Thread(
        target=perform_action,
        args=(source_folder, destination_folder, selected_extension, selected_action, progress_var, total_files)
    )
    thread.start()

    def check_thread():
        if thread.is_alive():
            app.after(100, check_thread)
        else:
            progress_bar.destroy()
            processed_files = len(list(destination_folder.rglob(f"*.{selected_extension}")))
            messagebox.showinfo("Done", f"{selected_action.lower()}ing process completed! Total number of files: {processed_files}")

    app.after(100, check_thread)
def clean_fields():
    source_var.set('')
    destination_var.set('')
    file_type_combobox.set('')
    extension_combobox.set('')
    action_combobox.set('')

# GUI setup
app = tk.Tk()
app.title("File Operation Application")
app.geometry("750x320")
app.resizable(False, False)
app.configure(bg='#F9F8ED')


# Load the image file
icon_path = "logo.ico"
if os.path.exists(icon_path):
    app.iconbitmap(default=icon_path)
else:
    print("Icon file not found, using default icon.")



style = ttk.Style()
style.theme_use('clam')
style.configure('PerformAction.TButton', font=('Helvetica', 11), background='#89C01D', foreground='white', borderwidth='1')
style.map('PerformAction.TButton', background=[('active', '#A1E025')])
style.configure('clean.TButton', font=('Helvetica', 11), background='red', foreground='white', borderwidth='1')
style.map('clean.TButton', background=[('active', 'orange')])
style.configure('Browse.TButton', font=('Helvetica', 11), background='#405DE6', foreground='white', borderwidth='1')
style.map('Browse.TButton', background=[('active', '#6B80FF')])
style.configure('TLabel', font=('Helvetica', 15), background='#F9F8ED', foreground='black')
style.configure('TEntry', font=('Helvetica', 15), borderwidth='2', fieldbackground='#ffffff', foreground='black')
style.configure('TCombobox', font=('Helvetica', 15), borderwidth='2', fieldbackground='#ffffff', foreground='black')
style.configure("Horizontal.TProgressbar", background='#41EA42', thickness=20)

file_types = ["Image", "Text", "Audio", "Video", "Program file", "Compressed"]
actions = ["Copy", "Move"]

action_label = ttk.Label(app, text="Action:")
action_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

action_combobox = ttk.Combobox(app, values=actions, height=15)
action_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

file_type_label = ttk.Label(app, text="File Type:")
file_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

file_type_combobox = ttk.Combobox(app, values=file_types)
file_type_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

extension_label = ttk.Label(app, text="Select Extension:")
extension_label.grid(row=1, column=1, padx=250, pady=10, sticky="w")

default_extensions = ["txt", "rtf", "docx", "csv"]
extension_combobox = ttk.Combobox(app, values=default_extensions)
extension_combobox.grid(row=1, column=1, padx=410, pady=10, sticky="w")

file_type_combobox.bind("<<ComboboxSelected>>", update_extension_options)

# source file
source_label = ttk.Label(app, text="Source Folder:")
source_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

source_var = tk.StringVar()
source_entry = ttk.Entry(app, textvariable=source_var, width=48)
source_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w", columnspan=2)

source_browse_button = ttk.Button(app, text="Browse", command=lambda: browse_button(source_var),style='Browse.TButton')
source_browse_button.grid(row=2, column=1, padx=448, pady=10, sticky="w")

# destination file
destination_label = ttk.Label(app, text="Destination Folder:")
destination_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

destination_var = tk.StringVar()
destination_entry = ttk.Entry(app, textvariable=destination_var, width=48)
destination_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w", columnspan=2)

destination_browse_button = ttk.Button(app, text="Browse", command=lambda: browse_button(destination_var),style='Browse.TButton')
destination_browse_button.grid(row=3, column=1, padx=448, pady=10, sticky="w")

# perform action button
perform_action_button = ttk.Button(app, text="Perform Action", command=perform_action_button ,style='PerformAction.TButton' )
perform_action_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

clean_button = ttk.Button(app, text="Clean", command=clean_fields, style='clean.TButton')
clean_button.grid(row=4, column=0, columnspan=2, padx=150, pady=10, sticky="w")


app.mainloop()