


# Explicit closing____________________________________________________
log = open('app_log.txt', 'r')          # open input file
output = open('filtered_log.txt', 'w')  # open output file
try:
    for entry in log:
        if any(keyword in entry for keyword in ('ERROR', 'WARNING')):   # for each entry in the input file containing the keywords
                output.write(entry + '\n')                              # Write the entry to the output file
finally:
    log.close()     # close input file
    output.close()  # close output file
    

# implicit closing____________________________________________________
with open('app_log.txt', 'r') as log:                                       # open input file
    with open('filtered_log.txt', 'w') as output:                           # open output file
        for entry in log:
            if any(keyword in entry for keyword in ('ERROR', 'WARNING')):
                output.write(entry + '\n')
# using the 'with' statement automatically closes the open files once they're out of scope
