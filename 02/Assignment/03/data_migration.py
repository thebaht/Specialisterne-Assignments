import csv
import re

col = 4
types = ['idx', 'name', 'email', 'money']
idx = []
names = []
emails = []
purchase = []
rows = [idx, names, emails, purchase]


def validate_row(row, col):
    i=0
    for f in row:
        try:
            if row[i].strip() == '':
                row.pop(i)
                row = validate_row(row, col)
                if validate_row(row, col) is None:
                    return None
                else:
                    continue
        except Exception:
            continue
    try:
        if len(row) != col:
            print(f"Row {ln}: Invalid # of columns")
            return None
    except Exception:
        return None
    return row

def validate_types(row, types):
    for v, t in zip(row, types):
        if t == 'idx':
            if not v.strip().isdigit():
                print(f"Row {ln}: id not a number")
                return False
            if not int(v) >= 0:
                print(f"Row {ln}: id <= 0")
                return False
            if not int(v) == ln-1:
                print(f"Row {ln}: id out of sequence")
                return False
        elif t == 'name':
            pattern = r'^(?:[a-zA-Z]+[ ])+(?:[a-zA-Z]+[\.]?)$'
            if re.match(pattern, v.strip()) is None:   
                print(f"Row {ln}: invalid name format")
                return False
        elif t == 'email':
            pattern = r'^\S+\@\w+\.\w+$' 
            if re.match(pattern, v.strip()) is None:   
                print(f"Row {ln}: invalid email format")
                return False
        elif t == 'money':
            try:
                float(v.strip()) 
                if float(v.strip()) <= 0:
                    print(f"Row {ln}: purchase_amount must be higher than 0")
                    return False
            except ValueError:
                print(f"Row {ln}: purchase_amount not a float")
                return False
    return True

with open('source_data.csv', 'r') as source:
    with open('destination_data.csv', 'w') as out:
        reader = csv.reader(source)
        writer = csv.writer(out, delimiter=',')
        header = next(reader)
        for x, c in zip(header, rows):
            c.append(x.strip())
            
        for ln, row in enumerate(reader, start=2):
            if not validate_row(row, col):
                continue
            
            if not validate_types(row, types):
                continue    

            for x, c in zip(row, rows):
                c.append(x.strip())
        print(10000-len(idx))
        writer.writerows(zip(idx,names, emails, purchase))