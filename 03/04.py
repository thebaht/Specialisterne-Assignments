import csv
from collections import defaultdict
import matplotlib.pyplot as plt

types = ['fen', 'line', 'depth', 'knodes', 'cp', 'mate'] 

def select(states):
    for entry in states:
        for v,t in zip(entry, types):
            if t == 'depth':
                d = int(v)
            elif t == 'mate':
                try:
                    if float(v) == 20.0:
                        yield d, float(v)
                except (ValueError, UnboundLocalError):
                    continue
            
                    
def eval(selected):
    a, c, max, min, freq = 0, 0, 0, 0, defaultdict(int)
    for d,m in selected:
        freq[d] += 1    
        a += d
        c += 1
    return a/c, c, max, min, freq

        
with open('less_evals.csv', 'r') as source: 
# with open('evals.csv', 'r') as source: 
    reader = csv.reader(source)
    header = next(reader)
    
    e = eval(select(reader))
    print(f"\nDepth for {e[1]} mate evaluations of 20.0: \n\tAverage:\t{e[0]}\n\tMax:\t{e[2]}\n\tMin:\t{e[3]}")
    freq = sorted(e[4].items(), key=lambda x: x)
    depths = [item[0] for item in freq]
    frequencies = [item[1] for item in freq]
    
    plt.figure(figsize=(15, 5))
    plt.bar(depths, frequencies, color='skyblue')   
    plt.title('Depth Frequency')                  
    plt.xlabel('Depth')                           
    plt.ylabel('Frequency')                           
    plt.tight_layout()
    plt.show()