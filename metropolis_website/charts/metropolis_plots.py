import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from numpy import ndarray, random
import math

FIGWIDTH = 6
FIGHEIGHT = 6
FONTSIZE = 12

plt.rcParams['figure.figsize'] = (FIGWIDTH, FIGHEIGHT)
plt.rcParams['font.size'] = FONTSIZE

plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE

data_start = 0
data_end = 1
data_points = 21
data = np.linspace(data_start, data_end, data_points)

def get_prob_dist_func(leftBound, rightBound, numPoints, distribution='norm'):
    data_points = np.linspace(leftBound, rightBound, numPoints)

    if distribution=='norm':
        pdf = [scipy.stats.norm.pdf(point)/numPoints for point in data_points]

    return pdf, ndarray.tolist(data_points)

def get_labels(pdf):
    labels = np.linspace(math.floor(pdf[0]), math.ceil(pdf[:1]), abs(math.floor(pdf[0])) + abs(math.ceil(pdf[:1])) + 1)
    return ndarray.tolist(labels)

    






print(data)

# prob_pdf = [uniform.pdf(point)/data_points for point in data]
prob_pdf = [scipy.stats.norm.pdf(point)/data_points for point in data]
print(prob_pdf)

plt.figure(figsize=(FIGWIDTH*3,FIGHEIGHT))
plt.subplot(3, 1, 1)
plt.plot(data, prob_pdf)
plt.ylabel('Probability')
plt.show()

tot_samples = 20

start_idx = random.randint(0, data_points) # Select random index of data array
markov_idx = [start_idx] # Initialize list of markov indicies
count = 0

for i in range(tot_samples):
    coin = random.randint(0,2)
    if coin:
        if markov_idx[count] == len(prob_pdf) - 1:   # check if the chain can go any more to the right
            markov_idx.append(markov_idx[count])    # append current value to chain
        elif prob_pdf[markov_idx[count] + 1] > prob_pdf[markov_idx[count]]:                     # check if prob to the right is greater
            markov_idx.append(markov_idx[count] + 1)                                  # append index of prob to the right
        else:
            if random.rand() < (prob_pdf[markov_idx[count] + 1] / prob_pdf[markov_idx[count]]): # probabilitically decide to go to the right
                markov_idx.append(markov_idx[count] + 1)                              # append index of prob to the right
            else:
                markov_idx.append(markov_idx[count])                                  # append current index
    else:
        if markov_idx[count] == 0:   # check if the chain can go any more to the left
            markov_idx.append(markov_idx[count])    # append current value to chain
        elif prob_pdf[markov_idx[count] - 1] > prob_pdf[markov_idx[count]]:                     # check if prob to the left is greater
            markov_idx.append(markov_idx[count] - 1)                                  # append index of prob to the right
        else:
            if random.rand() < (prob_pdf[markov_idx[count] - 1] / prob_pdf[markov_idx[count]]): # probabilitically decide to go to the left
                markov_idx.append(markov_idx[count] - 1)                              # append index of prob to the left
            else:
                markov_idx.append(markov_idx[count])                                  # append current index

    count += 1

print(markov_idx)
print(count)
# markov_idx.append(1)
# print(markov_idx)
