import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# list of names
names = [
    "Alexander", "Benjamin", "Charlotte", "Daniel", "Emily", "Frederik", 
    "Gabriel", "Hannah", "Isabella", "Jacob", "Katherine", "Liam", "Mia", 
    "Nathan", "Olivia", "Peter", "Quinn", "Rebecca", "Samuel", "Theresa", 
    "Ulysses", "Victoria", "William", "Xander", "Yasmine", "Zachary",
    "Amelia", "Aaron", "Sophia", "Noah", "Ava", "James", "Lucas", "Ethan", 
    "Ella", "David", "Elijah", "Aria", "Jackson", "Aiden", "Scarlett", 
    "Sofia", "Matthew", "Logan", "Abigail", "Grace", "Henry", "Isla", 
    "Ryan", "Evelyn", "Oliver", "Sebastian", "Harper", "Caleb", "Chloe", 
    "Julian", "Penelope", "Levi", "Victoria", "Dylan", "Aurora", "Luke", 
    "Hazel", "Isaac", "Samantha", "Theodore", "Lily", "Grayson", "Lillian", 
    "Joshua", "Layla", "Zoe", "Madison", "Owen", "Caroline", "Leo", 
    "Alice", "Mason", "Eleanor", "Wyatt", "Ellie", "Jack", "Nora", "Lucas",
    "Sarah", "Evan", "Luna", "Mila", "Eli", "Sadie", "Landon", "Addison",
    "Jaxon", "Piper", "Lincoln", "Stella", "Connor", "Grace", "Hudson", 
    "Ruby", "Carson", "Sophia", "Asher", "Kinsley", "Christian", "Brielle",
    "Maverick", "Vivian", "Nolan", "Emilia", "Hunter", "Camila", "Adrian", 
    "Archer", "Easton", "Emery", "Maddox", "Faith", "Roman", "Riley"
]

# Sort list of names by length then alphabetical, and print it
names = sorted(names, key=lambda x: (len(x), x))                        
print(f"\n\nNames sorted by length then alphabetical:\n{names}")        


# Create dictionary, as a defaultdict, with default values of 0, freq. 
# Iterate through each character c for each name in the list. For each c, add 1 to the value of freq[c].
# All characters are converted to lower case, so that counts for upper and lower case characters are combined.
freq = defaultdict(int)
for n in names:
    for c in n:
        freq[c.lower()] += 1                                            
print(f"\n\n(defaultdict) Frequency of characters in names:\n{freq}")

# Sort characters by their frequency descending.
freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
print(f"\n\nSorted Frequency of characters in names:\n{freq}")


# Create separate lists of characters and frequencies for plotting
characters = [item[0] for item in freq]
frequencies = [item[1] for item in freq]


'''
Matplotlib only ___________________________________________________________
'''
# Create a figure for a chart
plt.figure(figsize=(15, 5))

# Bar Chart
plt.subplot(1, 2, 1)                                # create subplot for multiple chars in the same window
plt.bar(characters, frequencies, color='skyblue')   # create bar chart with x-axis: characters | y-axis: frequencies
plt.title('Character Frequency')                    # bar chart title
plt.xlabel('Characters')                            # bar chart x-axis label
plt.ylabel('Frequency')                             # bar chart y-axis label

# Histogram
plt.subplot(1, 2, 2)                                # play histogram with a different index so it doesn't overlap with the bar chart.
plt.hist(frequencies, bins=range(1, max(frequencies) + 2), color='lightcoral', edgecolor='black')
plt.title('Character Frequency')
plt.xlabel('Frequency')
plt.ylabel('Count of Characters')

plt.tight_layout()  # adjusts padding and spacing around charts to make it look nicer


'''
Seaborn ___________________________________________________________________
'''
plt.figure(figsize=(15, 5))

sns.set_theme(style="whitegrid")    # sets appearence theme for matplotlib and seaborn stuff

# Bar Chart
plt.subplot(1, 2, 1)
sns.barplot(x=characters, y=frequencies, color='skyblue')
plt.title('Character Frequency')
plt.xlabel('Characters')
plt.ylabel('Frequency')

# Histogram
plt.subplot(1, 2, 2)
sns.histplot(frequencies, bins=range(1, max(frequencies) + 2), color='coral', kde=False)
plt.title('Character Frequency')
plt.xlabel('Frequency')
plt.ylabel('Count of Characters')

plt.tight_layout()


'''
Word Cloud ___________________________________________________________________
'''
plt.figure(figsize=(10, 5))

# Generate a word cloud from the defaultdict casted to standard dictionary.
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(freq))

# generate image from wordcloud
plt.imshow(wordcloud, interpolation='bilinear') #
plt.axis('off')  # Hide axes


'''
Name length analysis ___________________________________________________________________
'''
# Create a new dictionary, l, with default value 0, and for each length of a name, len(n), in the list of names, add 1 to l[len(n)]
l = defaultdict(int)
for n in names:
    l[len(n)] += 1
    
l_byValue = sorted(l.items(), key=lambda x: x[1], reverse=True)     # Sort l by the frequency of each name-length
print(f"\n\nFrequency of name length, sorted by frequency:\n{l_byValue}")

l_byKey = sorted(l.items(), key=lambda x: x[0])                     # Sort l by name-length
print(f"\n\nFrequency of name length, sorted by length:\n{l_byKey}")

# add the length of each name in the list of names, sorted by length, to the list, l_list.
l_list = []
for n in names:
    l_list.append(len(n))
l_median = l_list[int(len(l_list)/2)]   # finds the median length 
print(f"\n\nMedian length of name:\n{l_median}") 

# add all the lengts of names together and find the average length
t=0
for l in l_list:
    t += l
t=t/len(l_list)
print(f"\n\nAverage length of name:\n{t}")


# separate lists of name lengths and frequencies for plotting
length = [item[0] for item in l_byValue]
frequencies = [item[1] for item in l_byValue]

# create a bar chart to show the frequency of each name length.
plt.figure(figsize=(8, 5))
sns.barplot(x=length, y=frequencies, color='skyblue')
plt.title('Length Frequency')
plt.xlabel('Length')
plt.ylabel('Frequency')


# Show all the charts created up to this point in the program.
plt.show()