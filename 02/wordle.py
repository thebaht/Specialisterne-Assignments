import sys
import random
import re
import tkinter as tk
from tkinter import font

## Setup______________________________________________________
with open('Wordle Words.txt', 'r') as file:         # Open the provided txt file
    words = file.read().split()                     # Read text from the open file, split the string into a list of words and store the list

target = list(random.choice(words).upper())         # Global variable to store the word that needs to be guesses      
attempts = 0                                        # Global variable to track the number of attempted guesses



## Game logic_________________________________________________
'''
string -> (list<int, string>, int)
Compares 2 words. Returns a tuple that contains a list with the outcome for each character and the amount of correctly guessed characters.
The list contains tuples of (r, c), where r indicates correctness of c.
r = 1: correct char + correct index | r = 0: correct char + incorrect index | r = -1: incorrect char
'''
def compare(guess):
    global attempts                                     # Refers to global variable
    attempts = attempts + 1                            
    guess = list(enumerate(guess.strip().upper()))      # format guess to list<index, char> with all characters in uppercase and no leading/trailing whitespaces
    display = [None] * 5                                # Empty list of length 5, to store the result of the comparison
    score = 0                                           # Variable to store amount of correctly guesses characters.
    for i, c in guess:                                  
        try:                                            
            target.index(c)                             # If target contains c, return its first occuring index, otherwise throw a ValueError and fail to except.
            if target[i] == c:                          # Check if the index of c is the same in both target and guess.
                display[i] = (1,f" {c} ")               # Store a tuple containing an int to indicate correctness of character and c as a string with additional whitespace.
                score = score + 1                       
            else:
                display[i] = (0,f" {c} ")               
        except ValueError:                              
            display[i] = (-1,f" {c} ")                  
    return display, score                               

'''
(list<int, string>, tk.Frame) -> void
Add colored tk.Label's to a tk.Frame and display them in gui.
The variable r indicates correctness of the character c.
r = 1: correct char + correct index | r = 0: correct char + incorrect index | r = -1: incorrect char
''' 
def display(result, frame):
    for r, c in result:                                                     
        if r > 0:                                                           
            e = tk.Label(frame, text=c, bg="lightgreen", font=global_font)  # Create a label e, displaying the character c with a colored background, in the play-frame,
            e.pack(side=tk.LEFT)                                            # Display e in the play-frame, such that the label will stack from left to right instead of top to bottom.
        if r == 0:                                                          
            e = tk.Label(frame, text=c, bg="yellow", font=global_font)      
            e.pack(side=tk.LEFT)                                            
        if r < 0:                                                           
            e = tk.Label(frame, text=c, bg="lightgray", font=global_font)   
            e.pack(side=tk.LEFT)                                            

'''
int -> void
Checks if the game is resolved, and displays the result if so.
The variable r indicates how many characters were correctly guessed.
The global variable attempts indicates how many guesses have been attempted.
'''
def resolve(score):                                                 
    if score == 5:                                                                  # The entire word have been correctly guessed if score == 5 
        re = tk.Label(resolved, text="You win!", font=global_font, bg='darkgray')   # Create a label re, displaying the result of the game, in the resolved-frame,
        re.pack()                                                                   # Display re
    elif attempts == 6:                                                             # No attempts remains if attempts == 6.
        re = tk.Label(resolved, text="You lose!", font=global_font, bg='darkgray')  
        re.pack()                                                                   
    else:                                                                           # If the game hasn't been resolved
        entry.pack()                                                                # Display the entry-field
        
'''
void -> void
Starts a new game, by resetting the appropriate variables, choosing a new target word, and clearing frames of labels from the previous game
Newly created empty frames are not visible even when displayed.
'''
def newgame():                                      
    global attempts                                 # Refers to global variable
    global target                                   # Refers to global variable
    global frame                                    # Refers to global variable
    global resolved                                 # Refers to global variable
    attempts = 0                                    # Reset attempts to 0
    target = list(random.choice(words).upper())     # Choose a new random word, convert all characters to uppercase and convert the string to list<char>
    entry.pack()                                    # Display entry-field to accept new input
    frame.destroy()                                 # Destroy the play-frame and it's children.
    frame = tk.Frame(root)                          # Create a new play-frame in the main window.
    frame.pack(before=entry)                        # Displays the new play-frame, before the entry-field in the order.
    resolved.destroy()                              # Destroy, create and display new resolved-frame.
    resolved = tk.Frame(root)                       
    resolved.pack()                                

'''
void -> void
Læser input fra Entry boksen, matcher det med target, viser resultatet af gættet.
Reads input from entry-field, compares the input to target, and displays the result of the comparison.
'''
def entry_submit():
    entry.pack_forget()                 # Hides entry-field
    f = tk.Frame(frame)                 # Create a new frame, f, to display the result of the comparison in the play-frame.
    f.pack()                            # Display f
    word = entry.get()                  # Read input from entry-field
    result = compare(word)              # Compare input with target
    entry.delete(0, tk.END)             # Delete text from entry-field
    display(result[0], f)               # Display the result of the comparison
    resolve(result[1])                  # Check if the game has been resolved.

'''
event -> void
Validates the input from entry-field
'''
def validate_guess(event):
    global em                                                                                                       # Refers to global variable
    global err                                                                                                      # Refers to global variable
    word = entry.get().strip().upper()                                                                              # Stripts leading/trailing whitespace from input and converts it to uppercase.
    pattern1 = r'^[A-Z]*$'                                                                                          # Regex pattern matching strings containing only A-Z
    pattern2 = r'^\S{5}$'                                                                                           # Regex pattern matching strings containing only 5 characters
    if re.match(pattern1, word) is None:                                                                            # If pattern1 fails
        try:
            em.config(text="Only the letters A-Z are allowed.")                                                     # If em exists, set text to an appropriate error message.
        except (tk.TclError, NameError) as e:                                                                       # If em doesn't exist:
            em = tk.Label(root, text="Only the letters A-Z are allowed.", font=('Consolas', 14), bg='darkgray')     # Create a new label with an appropriate error message in the main window
        em.pack()                                                                                                   # Display the label below the play-frame                                                                                               
        entry.delete(0, tk.END)                                                                                     # Delete text from entry-field
    elif re.match(pattern2, word) is None:                                                                          # If pattern2 fails
        try:
            em.config(text="Your guess must be a 5-letter word.")                                                   
        except (tk.TclError, NameError) as e:                                                                      
            em = tk.Label(root, text="Your guess must be a 5-letter word.", font=('Consolas', 14), bg='darkgray')  
        em.pack()   
        entry.delete(0, tk.END)                                                                                   
    else:                                                                                                           # If input was accepted
        try:                                                                                                        # Try to delete an error message if it exists, otherwise submit input 
            em.destroy()  
        except NameError:
            entry_submit()
        else:                                                                                                       # Separate case because different exceptions can occur.
            entry_submit()      




## GUI_____________________________________________________________
root = tk.Tk()                          # Create main window
root.title("Wordle")                    # Set window title
root.geometry("400x600")                # Set window dimensions
root.config(bg='darkgray')              # Set window color

# Create and display Title label
title = tk.Label(root, text="Wordle", font=('Consolas', 32, 'bold'), bg='darkgray') 
title.pack(pady=10)

# Create a frame surrounding the play-frame to add a fixed size border
border = tk.Frame(root,  height=270, width=312, bd=3, highlightbackground='darkgray', highlightthickness=3)
border.pack_propagate(False)            # Prevents the frame from changing size with contained elements.
border.pack(padx=30, pady=30)

# Create and display play-frame in the border-frame
frame = tk.Frame(border)
frame.pack()

# Create a global Font for labels
global_font = font.Font(family='Consolas', size=24)

# Create a text-input field in the border-frame, the entry-field, and focus it.
entry = tk.Entry(border, width=16, font=global_font)   
entry.pack()
entry.focus()

entry.bind("<Return>", validate_guess)  # Binds the validate function to the keys <Enter>/<Return> when the entry-field is focused.

# Create and display the desolved-frame
resolved = tk.Frame(root)
resolved.pack()



# Create and display a new game-button in the mainwindow
button = tk.Button(root, text="New Game", command=newgame)
button.place(x=20, y=20)

                                        
# Start event loop
root.mainloop()                         

