import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

word1 = sys.argv[1]
word2 = sys.argv[2] #input()
word3 = sys.argv[3] #input()
word4 = sys.argv[4] #input()
word5 = sys.argv[5]  #input()

countWord1 = sys.argv[6]
countWord2 = sys.argv[7]
countWord3 = sys.argv[8]
countWord4 = sys.argv[9]
countWord5 = sys.argv[10]

words = [word1,word2,word3,word4,word5]
numbers = [int(countWord1),int(countWord2),int(countWord3),int(countWord4),int(countWord5)]

# Set Limits for the Y axis
low = min(numbers)
high = max(numbers)


# Add title and axis names
plt.bar(words,numbers)
plt.title('Frequency of Words')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.ylim(0,high+1)

# Show graphic
plt.show()
