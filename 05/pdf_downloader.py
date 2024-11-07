import pandas as pd
from os import walk, makedirs
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import Y, Scrollbar, font, ttk
from PIL import Image, ImageTk
import threading



source_path = 'GRI_2017_2020.xlsx'
output_path = './pdf-files/'
makedirs('pdf-files', exist_ok=True)

labels = {}
downloaded = set()
failed = set()


print(f'\nReading file..')
df = pd.read_excel(source_path, index_col='BRnum')
df = df[df.Pdf_URL.notnull() == True]
df = df[['Pdf_URL', 'Report Html Address']] # removes irrelevant columns. Not necessary to do, but it only adds 0.01s and feels cleaner.

for (dirpath, dirnames, filenames) in walk(output_path):
    downloaded.update(map(lambda x: x[:-4], filenames))

arrow_path = './icons/square-arrow-down.png'
check_path = './icons/square-check.png'
x_path = './icons/square-x.png'

root = tk.Tk()                          # Create main window
root.geometry("760x600")                # Set window dimensions
root.config(bg='gray6')              # Set window color

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
frame = tk.Frame(canvas, padx=24, pady=14, bg='gray6')

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


def download(path, brnum, url, alt_url=pd.NA):
    try:
        with requests.get(url, timeout=20, stream=True) as response:
            response.raise_for_status()
            if not response.content[:4] == b'%PDF':
                raise Exception
            with open(path, 'wb') as pdf:
                for chunk in response.iter_content(chunk_size=8192):
                    pdf.write(chunk)
                labels[brnum].config(image=check_icon)
                downloaded.add(brnum)
    except Exception as e:
        if pd.isna(alt_url):
            labels[brnum].config(image=x_icon)
            failed.add(brnum)  
        else:
            download(path, brnum, alt_url)

def main():
    with ThreadPoolExecutor() as executor:
        for brnum, row in df.head(20).iterrows():
        # for i, row in df.iterrows():
            if brnum in downloaded:
                labels[brnum].config(image=check_icon)
                continue
            path = output_path+brnum+'.pdf'
            executor.submit(download, path, brnum, row['Pdf_URL'], row['Report Html Address'])
            
    with open(output_path+'_status.txt', 'w') as output:
        for brnum, row in df.head(20).iterrows():
            if brnum in failed:
                status = 'Failed'
            else:
                status = 'Downloaded'
            output.write(f"{brnum}\t\t{status}\n")


for i, (brnum, row) in enumerate(df.head(20).iterrows()):
# for i, row in df.iterrows():
    row = i // 5
    col = i % 5
    label = tk.Label(frame, text=f"{brnum}", padx=5, image=arrow_icon, compound='right', font=global_font, fg='gray90', bg='gray6')
    label.grid(row=row, column=col, padx=6, pady=2)
    # label.pack(padx=44, pady=1)
    labels[brnum]=label

thread = threading.Thread(target=main)
thread.start()
root.mainloop()