import csv

def take_first_n_lines(input_file, output_file, n=1000000):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Copy the header first, if it exists
        header = next(reader, None)
        if header:
            writer.writerow(header)
            n -= 1  # Reduce count for header row if present
        
        # Write the first `n` lines
        for i, row in enumerate(reader):
            if i >= n:
                break
            writer.writerow(row)

# Usage
take_first_n_lines('evals.csv', 'less_evals.csv', 1000000)