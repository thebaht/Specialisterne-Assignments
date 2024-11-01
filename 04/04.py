import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import operator
import cProfile
import multiprocessing
import time

#create profiler
profiler = cProfile.Profile()

# order of columns for identifying data
types = ['fen', 'line', 'depth', 'knodes', 'cp', 'mate'] 

'''
(string, a, b) -> bool
Takes an operator as a string, and 2 values to compare. 
Returns the result of the comparison as a boolean. '''
def compare(o, a, b): 
    ops = {     # dictionary to look up operators from a string
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne   }
    try:
        r = ops[o](float(a), float(b)) # try to do the operation. Values casted to float for valid comparison in most cases
    except ValueError:
        try:
            r = ops[o](a, b)    # try without casting for edge cases
        except Exception:     
            r = False   # if values can't be compared, set return value to false
    return r    # return outcome

'''
(list<list<string>, (a,b), (c,d), (e,f), (g,h)) -> list
reads through the rows of strings and for each column in a row, checks whether the row can be selected.
If the last string in a row doesn't fail, a dictionary with the data from each column is yielded'''
def select(states, line=(None, None), depth=('==', None), centipawn=('==', None), mate=('==', None),):
    for entry in states:
        d = {}  # empty dictionary to hold row data
        for v,t in zip(entry, types):   # for each column in the row, zipped for headers for identification.
            if t == 'line':             # for the 'line' column
                if line[0] is not None: # if an argument to be filtered for has been provided
                    if not (line[0] == 'start' and v.startswith(line[1])) or (line[0] == 'end' and v.endswith(line[1])):    # if v doesn't either start or end with the provided string
                        break   # skip to next row if check failed
                d['line'] = v # otherwise store the data and continue to next column
                continue
            elif t == 'depth':  # for the depth column
                if depth[1] is not None:    # if an argument to be filtered for has been provided
                    if not compare(depth[0], v, depth[1]):  # if v doesn't pass the comparison with the provided value.
                        break  # skip to next row if check failed
                try:
                    d['depth'] = int(v) # otherwise try to cast and store the data
                except (ValueError, UnboundLocalError):
                    d['depth'] = None   # if v couldn't be casted, save the value as None
                continue
            elif t == 'centipawn': # for the centipawn column
                if centipawn[1] is not None:  # if an argument to be filtered for has been provided
                    if not compare(centipawn[0], v, centipawn[1]): # if v doesn't pass the comparison with the provided value.
                        break # skip to next row if check failed
                try:
                    d['centipawn'] = float(v) # otherwise try to cast and store the data
                except (ValueError, UnboundLocalError):
                    d['centipawn'] = None # if v couldn't be casted, save the value as None
                continue
            elif t == 'mate': # for the mate column
                if mate[1] is not None: # if an argument to be filtered for has been provided
                    if not compare(mate[0], v, mate[1]): # if v doesn't pass the comparison with the provided value.
                        break # skip to next row if check failed
                try:
                    d['mate'] = float(v) # otherwise try to cast and store the data
                except (ValueError, UnboundLocalError):
                    d['mate'] = None # if v couldn't be casted, save the value as None
                yield d # yield the dictionary with the data, since row passed all checks.
            
'''
csv.reader -> list<list>
selects rows where mate == 20.0. 
Counts the amount of rows, calculates their average/max/min depth, prints the result to console and returns lists of values for charts'''
def eval1(queue, file_path):
    try:
        with open(file_path, 'r') as source: # open file
            reader = csv.reader(source) # create reader
            next(reader)    # skip the header
            selected = select( reader, mate=('==', 20.0))   # select the rows 
            a, c, max, min, freq = 0, 0, 0, 0, defaultdict(int) # create variables for stats
            for l in selected:              # go through the selected rows for analysis
                freq[ l['depth'] ] += 1     # count frequency of depth
                a += l['depth']             # sum total depth
                c += 1                      # count the number of rows
                if max < l['depth']:        # check for maximum
                    max = l['depth']        # store maximum
                if min > l['depth']:        # check for minimum
                    min = l['depth']        # store minimum
            
            # print data to console
            print(f"\nEval1:\nDepth for {c} mate evaluations of 20.0: \n\tAverage:\t{a/c}\n\tMax:\t{max}\n\tMin:\t{min}")
            freq = sorted(freq.items(), key=lambda x: x)    # sort frequncies for nicer charts
            lists = [[item[0] for item in freq], [item[1] for item in freq]]    # organise depths and frequencies in list<list> for charts
            queue.put( lists)  # # put results in queue
            #Error messages if something breaks while running
    except FileNotFoundError:   
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to access '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

'''
csv.reader -> list<list>
selects rows where centipawn is empty. 
Counts the amount of rows, calculates their average/max/min depth, prints the result to console and returns lists of values for charts'''
def eval2(queue, file_path):
    try:
        with open(file_path, 'r') as source: # open file
            reader = csv.reader(source) # create reader
            next(reader)        # skip the header
            selected = select( reader, centipawn=('==', ''))  # select the rows 
            a, c, max, min, freq = 0, 0, 0, 0, defaultdict(int) # create variables for stats
            for l in selected:              # go through the selected rows for analysis
                freq[ l['depth'] ] += 1     # count frequency of depth    
                a += l['depth']             # sum total depth
                c += 1                      # count the number of rows
                if max < l['depth']:        # check for maximum
                    max = l['depth']        # store maximum
                if min > l['depth']:        # check for minimum
                    min = l['depth']        # store minimum
                
            # print data to console
            print(f"\nEval2:\nDepth for {c} evaluations where mate is certain: \n\tAverage:\t{a/c}\n\tMax:\t{max}\n\tMin:\t{min}")
            freq = sorted(freq.items(), key=lambda x: x)    # sort frequncies for nicer charts
            lists = [[item[0] for item in freq], [item[1] for item in freq]]   # organise depths and frequencies in list<list> for charts
            queue.put(lists)    # put results in queue
    #Error messages if something breaks while running
    except FileNotFoundError:   
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: You do not have permission to access '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# start the profiler     
profiler.enable()

# File to read from
file_path = 'less_evals.csv'       
# file_path = 'evals.csv'  

if __name__ == '__main__':
    # create queues for storing results
    queue1 = multiprocessing.Queue()    
    queue2 = multiprocessing.Queue()  
    
    # create processes for reading and processing data
    process1 = multiprocessing.Process(target=eval1, args=(queue1, file_path)) 
    process2 = multiprocessing.Process(target=eval2, args=(queue2, file_path)) 
    
    # start processes
    process1.start()
    process2.start() 

    # wait for both processes to finish and then terminate them
    process1.join()
    process2.join()
    
    # extract results
    e1 = queue1.get()
    e2 = queue2.get()
    
    print(f"\n_______________\ncProfile:\n")  # to make console more readable
    profiler.print_stats()  # print profiler stats
    



    # create bar chart for the 1st evaluation
    plt.figure(figsize=(15, 5))
    plt.bar(e1[0], e1[1], color='skyblue')   
    plt.title('Depth Frequency - Mate evaluation of 20.0')                  
    plt.xlabel('Depth')                           
    plt.ylabel('Frequency')                           
    plt.tight_layout()

    # create bar chart for the 2nd evaluation
    plt.figure(figsize=(15, 5))
    plt.bar(e2[0], e2[1], color='skyblue')   
    plt.title('Depth Frequency - When mate is certain')                  
    plt.xlabel('Depth')                           
    plt.ylabel('Frequency')                           
    plt.tight_layout()

    # Show both charts
    plt.show()
