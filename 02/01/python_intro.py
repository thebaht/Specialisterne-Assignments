import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

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

names = sorted(names, key=lambda x: (len(x), x))
print(f"\n\nNames sorted by length then alphabetical:\n{names}")


freq = {}
for n in names:
    for c in n:
        c = c.lower()
        freq[c] = freq.get(c, 0) + 1
print(f"\n\nFrequency of characters in names:\n{freq}")


freq = defaultdict(int)
for n in names:
    for c in n:
        freq[c.lower()] += 1      
print(f"\n\n(defaultdict) Frequency of characters in names:\n{freq}")


freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
print(f"\n\nSorted Frequency of characters in names:\n{freq}")


# Data for plotting
characters = [item[0] for item in freq]
frequencies = [item[1] for item in freq]



'''
Matplotlib only ___________________________________________________________
'''
# Create a bar chart
plt.figure(figsize=(15, 5))

# Bar Chart
plt.subplot(1, 2, 1)
plt.bar(characters, frequencies, color='skyblue')
plt.title('Character Frequency - Bar Chart')
plt.xlabel('Characters')
plt.ylabel('Frequency')

# Histogram
plt.subplot(1, 2, 2)
plt.hist(frequencies, bins=range(1, max(frequencies) + 2), color='lightcoral', edgecolor='black', alpha=0.7)
plt.title('Character Frequency - Histogram')
plt.xlabel('Frequency')
plt.ylabel('Count of Characters')



# Show the plot
plt.tight_layout()
# plt.show()

'''
Seaborn ___________________________________________________________________
'''
sns.set_theme(style="whitegrid")

# Create a bar chart
plt.figure(figsize=(15, 5))

# Bar Chart
plt.subplot(1, 2, 1)
sns.barplot(x=characters, y=frequencies, palette='Blues_d')
plt.title('Character Frequency - Bar Chart')
plt.xlabel('Characters')
plt.ylabel('Frequency')

# Histogram
plt.subplot(1, 2, 2)
sns.histplot(frequencies, bins=range(1, max(frequencies) + 2), color='coral', kde=False)
plt.title('Character Frequency - Histogram')
plt.xlabel('Frequency')
plt.ylabel('Count of Characters')


# Show the plot
plt.tight_layout()
# plt.show()

'''
Word Cloud ___________________________________________________________________
'''
# Step 4: Display the frequencies in a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(freq))

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Hide axes
# plt.show()


'''
Name length analysis ___________________________________________________________________
'''
l = defaultdict(int)
for n in names:
    l[len(n)] += 1
l_byValue = sorted(l.items(), key=lambda x: x[1], reverse=True)
l_byKey = sorted(l.items(), key=lambda x: x[0])
print(f"\n\nFrequency of name length, sorted by frequency:\n{l_byValue}")
print(f"\n\nFrequency of name length, sorted by length:\n{l_byKey}")

l_list = []
for n in names:
    l_list.append(len(n))
print(f"\n\nLength of names:\n{l_list}")
print(f"\n\nMedian length of name:\n{l_list[int(len(l_list)/2)]}")

t=0
for l in l_list:
    t += l
t=t/len(l_list)
print(f"\n\nAverage length of name:\n{t}")


length = [item[0] for item in l_byValue]
frequencies = [item[1] for item in l_byValue]

plt.figure(figsize=(8, 5))
plt.subplot(1, 1, 1)
sns.barplot(x=length, y=frequencies, palette='Blues_d')
plt.title('Length Frequency - Bar Chart')
plt.xlabel('Length')
plt.ylabel('Frequency')

plt.show()