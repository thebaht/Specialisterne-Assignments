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
output_path = './pdf-files/'            # Output folder to store the downloaded files
makedirs('pdf-files', exist_ok=True)    # Create output folder if it doesn't exist


labels = {}         # Dictionary that looks up gui labels by their BRNum
downloaded = set()  # Set of BRNums of completed downloads
failed = set()      # Set of BRNums of failed downloads
nums = set()        # Set of all BRNums

# This function retrieves the correct path of the icons when bundled inside the .exe
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# Paths to icons
arrow_path = resource_path('images/square-arrow-down.png')
check_path = resource_path('images/square-check.png')
x_path = resource_path('images/square-x.png')

# Variable to notify all threads to terminate
stop_event = threading.Event()


# Program functions ______________________________________________________________________________________________________________________________________________
def download(path, brnum, url, alt_url=pd.NA):
    """Downloads a pdf file from url, and updates the icon appropriately

    Args:
        path: Output path
        brnum: BRNum
        url: Download url
        alt_url (optional): Alternate download url
    """
    session = requests.Session()     # Create a request session
    try:
        with session.get(url, timeout=20, stream=True) as response: # Start the download as a stream
            response.raise_for_status()     # if download doesn't succeed, throw an exception
            if not response.content[:4] == b'%PDF': # Verify file type from the first 4 bytes of the file
                raise Exception                     # if not pdf, throw an exception
            with open(path, 'wb') as pdf:           # open output file
                for chunk in response.iter_content(chunk_size=1024):    # Handle file in chunks from stream
                    if stop_event.is_set():     # if program is closed
                        session.close()         # stop downloading
                        return                  # exit the function
                    pdf.write(chunk)            # write chunk to file
                labels[brnum].config(image=check_icon)  # Change gui icon to indicate success
                downloaded.add(brnum)       # add brnum to set of downloaded files
    except Exception as e:      # if download failed
        if pd.isna(alt_url):    # check if there is an alternate url
            labels[brnum].config(image=x_icon)  # change gui icon to indicate fail
            failed.add(brnum)   # add brnum to set of failed downloads
        else:                   # if alternate url exists
            download(path, brnum, alt_url)  # try downloading again with the alternate url
    finally:
        session.close() # after download has concluded, close the session


def daemon_thread_factory():    
    """Generates threads tagged as daemon, for main()
    """
    def create_daemon_thread(*args, **kwargs):
        thread = threading.Thread(*args, **kwargs)
        thread.daemon = True
        return thread
    return create_daemon_thread()


def main():
    """Iterates through the dataframe with links, starts the download in seperate threads, then writes the status of each file to a new file.
    """
    threads = []    # list to hold threads
    for brnum, row in df.iterrows():       # get the brnum and data from the dataframe
        if brnum in downloaded:                     # if file already downloaded
            labels[brnum].config(image=check_icon)  # update the icon
            continue                                # continue to next file
        
        while threading.active_count() > 100:       # wait until less than 100 threads are active, to avoid crashing the network with 21k threads.
            time.sleep(0.1) 
            
        t = threading.Thread(target=download, args=(output_path+brnum+'.pdf', brnum, row['Pdf_URL'], row['Report Html Address']), daemon=True)  # Create thread with a task
        threads.append(t)   # add thread to the list of threads
        t.start()   # start the thread
    
    # wait for all threads to finish
    [t.join() for t in threads]
    
    # update gui label to indicate download completion
    global status_label2
    status_label2.config(text='Complete!')  
    
    # write the brnum and download status of each pdf to a file
    with open(output_path+'_status.txt', 'w') as output:    
        for brnum in nums:
            if brnum in failed:
                status = 'Failed'
            else:
                status = 'Downloaded'
            output.write(f"{brnum}\t\t{status}\n")
            

# GUI ______________________________________________________________________________________________________________________________________________
def on_close():
    """Function to handle closing the program"""
    stop_event.set()            # notify threads to terminate
    root.destroy()              # Destroy the main Tkinter window
    sys.exit('Exiting..')       # Terminate the program


root = tk.Tk()                          # Create main window
root.geometry("740x585")                # Set window dimensions
root.config(bg='gray6')              # Set window color
root.protocol("WM_DELETE_WINDOW", on_close) # call on_close() when the window is closed

# Open the icons as ImageTk.PhotoImage
arrow_icon = ImageTk.PhotoImage(Image.open(arrow_path))
check_icon = ImageTk.PhotoImage(Image.open(check_path))
x_icon = ImageTk.PhotoImage(Image.open(x_path))

# Font for labels
global_font = font.Font(family='Verdana', size=12)


# Create a style for the scrollbar
style = ttk.Style(root)
style.theme_use('default')

# Customize the colors of scrollbar
style.configure("Vertical.TScrollbar",
                background="gray35",
                troughcolor="gray6",
                bordercolor='gray6',
                relief='flat',
                troughrelief='flat',
                width=8,
                gripcount=0)

# Make scrollbar colors consistent when hovered or inactive.
style.map("Custom.Vertical.TScrollbar",
          background=[("active", "gray35"), ("!active", "gray35")],
          troughcolor=[("active", "gray6"), ("!active", "gray6")])

# removes arrow buttons from the endges of scrollbar
style.layout("Custom.Vertical.TScrollbar",
             [('Vertical.Scrollbar.trough', {'children':
                 [('Vertical.Scrollbar.thumb', {'unit': '1', 'sticky': 'nswe'})],
                 'sticky': 'nswe'})])


canvas = tk.Canvas(root, bg='gray6', bd=3, highlightbackground='gray6', highlightthickness=3)   # create canvas to allow a frame to be scrollable
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")    # create scrollbar
frame = tk.Frame(canvas, padx=24, pady=0, bg='gray6')   # create frame to hold labels

# function to scroll on the canvas
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# Bind mouse wheel to scrolling
canvas.bind_all("<MouseWheel>", on_mouse_wheel)       # Windows

# bind the frame to the boundingbox of the canvas
frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)


canvas.create_window((0, 0), window=frame, anchor="nw") # place frame on canvas as a window
canvas.configure(yscrollcommand=scrollbar.set)  # connect vertical scrolling on the frame to the scrollbar

scrollbar.pack(side="right", fill="y")      # place scrollbar on the right side of the window
canvas.pack(side="left", fill="both", expand=True)  # place canvas on left side

# Show all labels
def filter_all():
    for brnum in nums:          # for all brnums
        labels[brnum].grid()    # place their label, where it was previously placed on the grid

# show only labels with completed downloads
def filter_sucess():
    for brnum in nums:
        if brnum in downloaded:
            labels[brnum].grid()        # place their label, where it was previously placed on the grid
        else:
            labels[brnum].grid_remove() # remove label from the grid

# show only labels for downloads still in progress
def filter_progress():
    for brnum in nums:
        if brnum in downloaded | failed:
            labels[brnum].grid_remove()
        else:
            labels[brnum].grid()

#show only labels for failed downloads
def filter_failed():
    for brnum in nums:
        if brnum in failed:
            labels[brnum].grid()
        else:
            labels[brnum].grid_remove()


banner = tk.Frame(root, pady=24, bg='gray6')    # frame to hold ui elements in the top of the window
banner.pack(before=canvas, fill='x')            # place it over canvas
status_container = tk.Frame(banner, padx=34, bg='gray6')    # frame to hold labels that indicate program status
status_container.pack(side='left')                          
status_label1 = tk.Label(status_container, text='Download: ', font=('Verdana', 14), fg='gray90', bg='gray6')    # non-italic part of the text that indicate program status
status_label1.pack(side='left')
status_label2 = tk.Label(status_container, text='Getting ready', font=('Verdana', 14, 'italic'), fg='gray90', bg='gray6')   # italic part of the text that indicate program status
status_label2.pack(side='left')
container_buttons = tk.Frame(banner, padx=45, bg='gray6')       # frame to hold filter label + buttons
container_buttons.pack(side='right')
filter_label = tk.Label(container_buttons, text='Filter:', padx=10, font=global_font, fg='gray90', bg='gray6')  # filter label
filter_label.grid(row=0, column=0)
button_all = tk.Button(container_buttons, text="All", command=filter_all)   # show all button
button_all.grid(row=0, column=1)
button_complete = tk.Button(container_buttons, text="Completed", command=filter_sucess) # completed downloads button
button_complete.grid(row=0, column=2)
button_progress = tk.Button(container_buttons, text="In progress", command=filter_progress) # downloads in progress button
button_progress.grid(row=0, column=3)
button_failed = tk.Button(container_buttons, text="Failed", command=filter_failed)  # failed downloads button
button_failed.grid(row=0, column=4)


# Handle input file ________________________________________________________________________________________________________________________________
source_path = filedialog.askopenfilename(   # open explorer window to request a file to be selected
    initialdir=os.getcwd(),
    title="Select a File",
    filetypes=(("Microsoft Excel Worksheet", "*.xlsx"), ("All Files", "*.*"))
)

print(f'\nReading file..')
df = pd.read_excel(source_path, index_col='BRnum')  # read .xlxs file to a dataframe and use BRNum as the index
df = df[df.Pdf_URL.notnull() == True]   # remove cells that doesn't contain a link to a pdf
df = df[['Pdf_URL', 'Report Html Address']] # removes irrelevant columns. Not necessary to do, but it only adds 0.01s and feels cleaner.

for (dirpath, dirnames, filenames) in walk(output_path):    # retrieve information for files in output directory
    downloaded.update(map(lambda x: x[:-4], filenames))     # add filename without extension to set of downloaded brnums

status_label2.config(text='In Progress..')      # update gui label to indicate download starting
for i, (brnum, row) in enumerate(df.iterrows()):   # iterate through dataframe while adding an index to each entry
    r = i // 5      # determine which row to place a new label
    c = i % 5       # determine which column to place new label
    label = tk.Label(frame, text=f"{brnum}", padx=5, image=arrow_icon, compound='right', font=global_font, fg='gray90', bg='gray6') # create new label with brnum + downloading icon
    label.grid(row=r, column=c, padx=6, pady=2) # place label at the determined spot in the grid
    labels[brnum]=label # add reference to label in labels
    nums.add(brnum) # add brnum to set of all brnums
    

# start main program logic _________________________________________________________________________________________________________________________
thread = threading.Thread(target=main, daemon=True) # run main() in a different thread than gui, to ensure gui responsiveness
thread.start()  
root.mainloop() # start gui