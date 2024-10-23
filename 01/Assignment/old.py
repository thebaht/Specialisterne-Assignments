import sys
import random
import re
import tkinter as tk

## Setup______________________________________________________

# ANSI Color escape sequences til at farve output
GREEN = "\x1b[38;2;0;0;0m\x1b[48;2;0;255;0m"        # Sort tekst, Grøn baggrund     
YELLOW = "\x1b[38;2;0;0;0m\x1b[48;2;255;255;0m"     # Sort tekst, Gul baggrund
GRAY = "\x1b[38;2;255;255;255m\x1b[48;2;60;60;60m"  # Hvid tekst, Grå baggrund
RESET = '\x1b[0m'                                   # Reset tekst farver til default

with open('Wordle Words.txt', 'r') as file:         # Åben .txt filen
    words = file.read().split()                     # Læs tekst fra filen, opdel den lange string i en liste af ord og gem listen i variablen

target = list(random.choice(words).upper())              
attempts = 6     
print(''.join(target)) 

## Helper functions____________________________________________
'''
(guess: List<int, char>, target: List<char>)  ->  (list<string>, int)
Sammenlign 2 ord. Guess er spillerents input og target er ordet der skal gættes.        '''
def match(guess, target):
    display = [None] * 5                                # Initialiser tom liste til opbevaring af resultat
    score = 0                                           # Initialiser variable til antal af korrekte bogstaver i korrekt position
    for i, c in guess:                                  # Iterer gennem guess og evaluer hver tuple
        try:                                            
            target.index(c)                             # Hvis target indeholder c, return dets første index, ellers smider den en ValueError og skipper til linje 29
            if target[i] == c:                          # check om c har samme index i guess og target
                display[i] = f"{GREEN} {c} {RESET}"     # Gem c som en grøn farvet string i display med samme index som c.
                score = score + 1                       # tilføj 1 til antal korrekt gættede bogstaver
            else:
                display[i] = f"{YELLOW} {c} {RESET}"    # Gem c som en gul farvet string i display med samme index som c.
        except ValueError:                              
            display[i] = f"{GRAY} {c} {RESET}"          # Gem c som en grå farvet string i display med samme index som c.
    return display, score                               


'''
word: string  ->  bool
bruger regex til at validere en string, og printe en error message hvis den fejler.     '''
def validate_guess(word):
    if word in ['QUIT', 'EXIT', 'Q']:                                       # Valider input ved at checke om input er en af de 4 strings.
            print(f"\nExiting game..\n\nThanks for playing")
            sys.exit(0)
    pattern1 = r'^[A-Z]*$'                                  # Regex pattern til at checke om ordet indeholder andre characters end bogstaverne a-z
    pattern2 = r'^\S{5}$'                                   # Regex pattern til at checke om ordet er 5 bogstaver langt 
    if re.match(pattern1, word) is None:                    # Hvis ordet ikke matcher pattern1, print error message og return False
        print(f"Only the letters A-Z are allowed.\n")       # print error message
        return False                                        # return False
    if re.match(pattern2, word) is None:                    # Hvis ordet ikke matcher pattern2
        print(f"Your guess must be a 5-letter word.\n")     # print error message
        return False                                        # return False
    return True                                             # Ordet har passed begge checks, return True.



## Game logic__________________________________________________
'''
None  ->  None
Kører et spil.                                                                          '''
def play():
    ongoing = True                                              # Variable til at holde øje med om spillet stadig er igang
    attempts = 6                                                # Variable til at opbevare antal gæt tilbage
    target = list(random.choice(words).upper())                 # Vælg et tilfældigt ord fra listen, sæt alle characters til upper case og konverter string til list<char>
    print(f'\n_____________________________\n')                 # print linje til at seperarer spil
    while ongoing:                                              # Check at spillet stadig er igang
        while True:                                             # Loop indtil input er accepteret
            guess = input("Type your guess: ").strip().upper()  # Request input fra spilleren med en besked. Når det er modtaget; fjern whitespace og sæt characters til upper case
            if validate_guess(guess):                             # Kør funktionen til at validere input med input string.
                break                                           # Hvis input blev valideret, break while loop, ellers gå tilbage til starten af loop.
        result = match(list(enumerate(guess)), target)          # Konverter input string til list<index, char> og match listen med ordet der skal gættes 
        print(''.join(result[0]))                               # Sammensætter listen med de farvede resultater til 1 string og printer den.
        
        if result[1] == 5:                                      # Check om ordet var korrekt gættet
            print(f"You win!\n")                                # Print resultatet af spillet: spilleren vandt 
            ongoing = False                                     # Sæt ongoing til False for at afslutte spillet
        else:                                                   # Hvis ordet ikke var korrekt gættet
            attempts = attempts-1                               # Reducer antal gæt tilbage
            if attempts == 0:                                   # Check om spilleren har flere gæt tilbage
                print(f"\nYou lose!\n")                         # Print resultatet af spillet: spilleren tabte
                ongoing = False                                 # Sæt ongoing til False for at afslutte spillet
            else:                                               # Hvis spilleren har flere gæt tilbage
                print(f"Chances remaining: {attempts}\n")       # Print antal gæt tilbage







## Program logic________________________________________________
play()                                                                              # Start det første spil når programmet køres.
while True:                                                                         # Loop indtil ikke spil ikke længere skal startes
    while True:                                                                     # Loop indtil input er accepteret
        answer = input("Do you want to play another game? ").strip().lower()        # Request input fra spilleren med en besked. Når det er modtaget; fjern whitespace og sæt characters til lower case
        if answer in ['yes', 'no', 'y', 'n']:                                       # Valider input ved at checke om input er en af de 4 strings.
            break                                                                   # Hvis input blev valideret, break loop
        else:                                                                       # Hvis input ikke blev valideret
            print("Invalid input. Accepted answers are 'yes', 'y', 'no', 'n'\n")    # Print error message
    if answer in ['yes', 'y']:                                                      # Hvis input er ja
        play()                                                                      # start et nyt spil
    else:                                                                           # ellers
        print(f"\nThanks for playing!")                                             # print message
        break                                                                       # Break loop og lad programmet afslutte.
