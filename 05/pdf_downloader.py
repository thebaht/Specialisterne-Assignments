import pandas as pd
import os
from os import walk, makedirs
import requests
import tkinter as tk
from tkinter import font, ttk, filedialog
from PIL import Image, ImageTk
import threading
import sys
import time


# Setup ______________________________________________________________________________________________________________________________________________
source_path = 'GRI_2017_2020.xlsx'
output_path = './pdf-files/'
makedirs('pdf-files', exist_ok=True)


labels = {}
downloaded = set()
failed = set()
nums = set()

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder _MEIPASS where it stores bundled files
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# Use the function to get the correct path to the images
arrow_path = resource_path('images/square-arrow-down.png')
check_path = resource_path('images/square-check.png')
x_path = resource_path('images/square-x.png')



stop_event = threading.Event()


# Program functions ______________________________________________________________________________________________________________________________________________
def download(path, brnum, url, alt_url=pd.NA):
    session = requests.Session()
    try:
        with session.get(url, timeout=20, stream=True) as response:
            response.raise_for_status()
            if not response.content[:4] == b'%PDF':
                raise Exception
            with open(path, 'wb') as pdf:
                for chunk in response.iter_content(chunk_size=1024):
                    if stop_event.is_set():
                        session.close()
                        return
                    pdf.write(chunk)
                labels[brnum].config(image=check_icon)
                downloaded.add(brnum)
    except Exception as e:
        if pd.isna(alt_url):
            labels[brnum].config(image=x_icon)
            failed.add(brnum)  
        else:
            download(path, brnum, alt_url)
    finally:
        session.close()

def daemon_thread_factory():
    def create_daemon_thread(*args, **kwargs):
        thread = threading.Thread(*args, **kwargs)
        thread.daemon = True
        return thread
    return create_daemon_thread()

def main():
    threads = []
    for brnum, row in df.iterrows():
        if brnum in downloaded:
            labels[brnum].config(image=check_icon)
            continue
        
        while threading.active_count() > 100:
            time.sleep(0.1) 
            
        t = threading.Thread(target=download, args=(output_path+brnum+'.pdf', brnum, row['Pdf_URL'], row['Report Html Address']), daemon=True)
        threads.append(t)
        t.start()
    
    [t.join() for t in threads]
    global status_label2
    status_label2.config(text='Complete!')
    
    with open(output_path+'_status.txt', 'w') as output:
        for brnum in nums:
            if brnum in failed:
                status = 'Failed'
            else:
                status = 'Downloaded'
            output.write(f"{brnum}\t\t{status}\n")
            

# GUI ______________________________________________________________________________________________________________________________________________
def on_close():
    """Callback function to handle window close."""
    stop_event.set()
    root.destroy()  # Destroy the main Tkinter window
    sys.exit('Exiting..')     # Ensure the program terminates completely

root = tk.Tk()                          # Create main window
root.geometry("740x585")                # Set window dimensions
root.config(bg='gray6')              # Set window color
root.protocol("WM_DELETE_WINDOW", on_close)

arrow_icon = ImageTk.PhotoImage(Image.open(arrow_path))
check_icon = ImageTk.PhotoImage(Image.open(check_path))
x_icon = ImageTk.PhotoImage(Image.open(x_path))

global_font = font.Font(family='Verdana', size=12)


# Create a style for the scrollbar
style = ttk.Style(root)
style.theme_use('default')

# Customize the colors
style.configure("Vertical.TScrollbar",
                background="gray35",
                troughcolor="gray6",
                bordercolor='gray6',
                relief='flat',
                troughrelief='flat',
                width=8,
                gripcount=0)

style.map("Custom.Vertical.TScrollbar",
          background=[("active", "gray35"), ("!active", "gray35")],
          troughcolor=[("active", "gray6"), ("!active", "gray6")])

style.layout("Custom.Vertical.TScrollbar",
             [('Vertical.Scrollbar.trough', {'children':
                 [('Vertical.Scrollbar.thumb', {'unit': '1', 'sticky': 'nswe'})],
                 'sticky': 'nswe'})])

canvas = tk.Canvas(root, bg='gray6', bd=3, highlightbackground='gray6', highlightthickness=3)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
frame = tk.Frame(canvas, padx=24, pady=0, bg='gray6')

# Function to scroll on Windows (mouse wheel event binding)
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Bind mouse wheel events to scroll on different OS
canvas.bind_all("<MouseWheel>", on_mouse_wheel)       # Windows

frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)


def filter_all():
    for brnum in nums:
        labels[brnum].grid()

def filter_sucess():
    for brnum in nums:
        if brnum in downloaded:
            labels[brnum].grid()
        else:
            labels[brnum].grid_remove()

def filter_progress():
    for brnum in nums:
        if brnum in downloaded | failed:
            labels[brnum].grid_remove()
        else:
            labels[brnum].grid()

def filter_failed():
    for brnum in nums:
        if brnum in failed:
            labels[brnum].grid()
        else:
            labels[brnum].grid_remove()

banner = tk.Frame(root, pady=24, bg='gray6')
banner.pack(before=canvas, fill='x')
status_container = tk.Frame(banner, padx=34, bg='gray6')
status_container.pack(side='left')
status_label1 = tk.Label(status_container, text='Download: ', font=('Verdana', 14), fg='gray90', bg='gray6')
status_label1.pack(side='left')
status_label2 = tk.Label(status_container, text='Getting ready', font=('Verdana', 14, 'italic'), fg='gray90', bg='gray6')
status_label2.pack(side='left')
container_buttons = tk.Frame(banner, padx=45, bg='gray6')
container_buttons.pack(side='right')
filter_label = tk.Label(container_buttons, text='Filter:', padx=10, font=global_font, fg='gray90', bg='gray6')
filter_label.grid(row=0, column=0)
button_all = tk.Button(container_buttons, text="All", command=filter_all)
button_all.grid(row=0, column=1)
button_complete = tk.Button(container_buttons, text="Completed", command=filter_sucess)
button_complete.grid(row=0, column=2)
button_progress = tk.Button(container_buttons, text="In progress", command=filter_progress)
button_progress.grid(row=0, column=3)
button_failed = tk.Button(container_buttons, text="Failed", command=filter_failed)
button_failed.grid(row=0, column=4)


# Handle input file ________________________________________________________________________________________________________________________________
source_path = filedialog.askopenfilename(
    initialdir=os.getcwd(),
    title="Select a File",
    filetypes=(("Microsoft Excel Worksheet", "*.xlsx"), ("All Files", "*.*"))
)

print(f'\nReading file..')
df = pd.read_excel(source_path, index_col='BRnum')
df = df[df.Pdf_URL.notnull() == True]
df = df[['Pdf_URL', 'Report Html Address']] # removes irrelevant columns. Not necessary to do, but it only adds 0.01s and feels cleaner.

for (dirpath, dirnames, filenames) in walk(output_path):
    downloaded.update(map(lambda x: x[:-4], filenames))

status_label2.config(text='In Progress..')
for i, (brnum, row) in enumerate(df.iterrows()):
    r = i // 5
    c = i % 5
    label = tk.Label(frame, text=f"{brnum}", padx=5, image=arrow_icon, compound='right', font=global_font, fg='gray90', bg='gray6')
    label.grid(row=r, column=c, padx=6, pady=2)
    labels[brnum]=label
    nums.add(brnum)
    

# start main program logic _________________________________________________________________________________________________________________________
thread = threading.Thread(target=main, daemon=True)
thread.start()
root.mainloop()