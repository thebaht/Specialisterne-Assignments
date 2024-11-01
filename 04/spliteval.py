import csv

'''
(string, string, int) -> ()
Writes the first n amount of lines from source into a new file.
Takes the filepath for the source file, the new file, and the amount of lines to copy.
'''
def take_n_lines(source_file, output_file, n=1000000):
    with open(source_file, 'r') as source, open(output_file, 'w', newline='') as output:     # open files
        reader = csv.reader(source) # create reader
        writer = csv.writer(output) # create writer
        
        # Read and write the header 
        header = next(reader, None)
        if header:
            writer.writerow(header)
            n -= 1  # deincrement n
        
        # Read and write the specified amount of lines
        for i, row in enumerate(reader):
            if i >= n:
                break
            writer.writerow(row)    # write the line

# call the function with the desired files and amount of lines
take_n_lines('evals.csv', 'smallest_evals.csv', 840000) 