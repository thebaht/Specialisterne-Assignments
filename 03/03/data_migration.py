import csv
import re

# Setup ____________________________________________________
# Variables for validation
col = 4                                     # amount of columns
types = ['idx', 'name', 'email', 'money']   # order of columns for data validation

# nested lists to hold output data
idx = []
names = []
emails = []
purchase = []
rows = [idx, names, emails, purchase]

'''
list<str> -> list<str>
Validates the amount of non-empty columns in a row.
If a row has an empty column, remove it and re-validate recursively.
'''
def validate_row(row):
    i=0
    for f in row:
        if row[i].strip() == '':    # if column is empty at index i
            row.pop(i)              # remove the column from the row
            row = validate_row(row) # Recursively re-validate the row
            if row is None:         # if row couldn't be validated, return None
                return None
            else:
                continue      
    if len(row) != col:                             # if the amount of non-empty columns is incorrect
        print(f"Row {ln}: Invalid # of columns")    # Error message
        return None                                 # Return None
    return row

'''
list<str> -> bool
Validates the data in each column of a row.
'''
def validate_types(row):
    for v, t in zip(row, types):                    # Iterate through the row and types zipped together for column identification
        if t == 'idx':                              # if the column is the id
            if not v.strip().isdigit():             # if id is not a digit
                print(f"Row {ln}: id not a number") 
                return False
            if not int(v) >= 0:                     # if id is not positive
                print(f"Row {ln}: id <= 0")
                return False
            if not int(v) == ln-1:                  # if id is out of sequence
                print(f"Row {ln}: id out of sequence")
                return False
        elif t == 'name':                               # if the column is the name
            pattern = r'^(?:[a-zA-Z]+[ ])+(?:[a-zA-Z]+[\.]?)$'  
            if re.match(pattern, v.strip()) is None:    # if name doesn't match the pattern
                print(f"Row {ln}: invalid name format") 
                return False
        elif t == 'email':                              # if the column is the email
            pattern = r'^\S+\@\w+\.\w+$'                # regex pattern to validate name
            if re.match(pattern, v.strip()) is None:    # if email doesn't match the pattern
                print(f"Row {ln}: invalid email format")
                return False
        elif t == 'money':                              # if the column is the purchase_amount
            try:
                float(v.strip())                        # attempt to cast the string to float
                if not float(v.strip()) >= 0:           # if casted float is not positive
                    print(f"Row {ln}: purchase_amount must be higher than 0")
                    return False
            except ValueError:                          # if string couldn't be casted to float
                print(f"Row {ln}: purchase_amount not a float")
                return False
    return True

'''
main program loop
'''
with open('source_data.csv', 'r') as source:        # open input file
    with open('destination_data.csv', 'w') as out:  # open output file
        reader = csv.reader(source)                 # create reader object for the input
        writer = csv.writer(out, delimiter=',')     # create writer object for the output
        header = next(reader)                       # Store column labels from input
        for x, c in zip(header, rows):              # Add the column labels to the top of output data lists
            c.append(x.strip())
            
        for ln, row in enumerate(reader, start=2):  # Starting at line 2 in the input, read through each row
            if not validate_row(row):               # validate amount of columns, 
                continue
            
            if not validate_types(row):             # validate data in each column
                continue    

            for x, c in zip(row, rows):             # Add each column in the row to the appropriate nested list in the output data lists
                c.append(x.strip())
                
        print(f"\n\nEntries removed:\n{10000-len(idx)}")    # print how many entries were removed.
        
        writer.writerows(zip(idx,names, emails, purchase))  # zip nested output data lists together and write them to output file