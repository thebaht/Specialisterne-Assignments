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

arrow_path = './icons/square-arrow-down.png'
check_path = './icons/square-check.png'
x_path = './icons/square-x.png'


root = tk.Tk()                          # Create main window
root.geometry("200x300")                # Set window dimensions
root.config(bg='gray6')              # Set window color

frame = tk.Frame(root)
frame.pack()

arrow_icon = ImageTk.PhotoImage(Image.open(arrow_path))
check_icon = ImageTk.PhotoImage(Image.open(check_path))
x_icon = ImageTk.PhotoImage(Image.open(x_path))

global_font = font.Font(family='Verdana', size=12)

for (dirpath, dirnames, filenames) in walk(output_path):
    downloaded.update(map(lambda x: x[:-4], filenames))



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
        for i, row in df.head(9).iterrows():
            if i in downloaded:
                labels[i].config(image=check_icon)
                continue
            path = output_path+i+'.pdf'
            executor.submit(download, path, i, row['Pdf_URL'], row['Report Html Address'])


df = pd.read_excel(source_path, index_col='BRnum')
df = df[df.Pdf_URL.notnull() == True]
df = df[['Pdf_URL', 'Report Html Address']] # removes irrelevant columns. Not necessary to do, but it only adds 0.01s and feels cleaner.


for i, row in df.head(9).iterrows():
    label = tk.Label(frame, text=f"{i}", image=arrow_icon, compound='right', font=global_font, fg='gray90', bg='gray6')
    label.pack()
    #! duplicate for scroll text 
    label_alt = tk.Label(frame, text=f"{i}", image=arrow_icon, compound='right', font=global_font, fg='gray90', bg='gray6')
    label_alt.pack()
    #! - - - - - - - - - - - - - 
    
    labels[i]=label

thread = threading.Thread(target=main)
thread.start()
root.mainloop()