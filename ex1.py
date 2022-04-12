# Hadas Babayov 322807629

import matplotlib.pyplot as plt
import numpy
import numpy as np
import sys

# This function get list of values, and show this values in graph.
def showGraph(listOfValues):
    x = list(range(len(listOfValues)))
    plt.plot(x, listOfValues, c='gray')
    plt.ylabel('Loss average')
    plt.xlabel('Num of iteration')
    plt.xticks(x, x)
    plt.show()

# This function get list of values and return the minimum value.
def findMin(list):
    min = list[0]
    for i in range(len(list)):
        if list[i] < min:
            min = list[i]
    return min

# This function calculate the average of loss.
def loss(pixels, cluster, z):
    sumOfDistance = 0
    counter = 0
    for i in range(len(z)):
        for j in range(len(cluster)):
            if cluster[j] == i:
                counter += 1
                d = (pixels[j][0] - z[i][0]) ** 2 + (pixels[j][1] - z[i][1]) ** 2 + (pixels[j][2] - z[i][2]) ** 2
                sumOfDistance += d
    return sumOfDistance/counter

# This function calculate the new center centroids according to the cluster.
def findCenterCentroids(pixels, cluster, z):
    centerCendroids = np.zeros((len(z),3))
    k = len(z)

    for i in range(k):
        sumPixelsByClusters = 0
        numOfPixels = 0
        for j in range(len(cluster)):
            if cluster[j] == i:
                sumPixelsByClusters += pixels[j]
                numOfPixels += 1
        if numOfPixels == 0:
            centerCendroids[i] = (z[i])
        else:
            ave = sumPixelsByClusters/numOfPixels
            centerCendroids[i] = (ave)
    return centerCendroids

# Check if the new center centroids and the old one - are equal or not.
def isEqual(z, newCenters):
    k = len(z)
    for i in range(k):
        if z[i][0] != newCenters[i][0] or z[i][1] != newCenters[i][1] or z[i][2] != newCenters[i][2]:
            return False
    return True

# This function write the result to the file.
def writeToFile(newCenter, file):
    arr = numpy.array(newCenter).round(4)
    file.write(f"[iter {countIteration}]:{','.join([str(i) for i in arr])}\n")

image_fname, centroids_fname, out_fname = sys.argv[1], sys.argv[2], sys.argv[3]
z = np.loadtxt(centroids_fname)  # z=k

orig_pixels = plt.imread(image_fname)
pixels = orig_pixels.astype(float) / 255
pixels = pixels.reshape(-1, 3)

diff = 1
cluster = np.zeros(pixels.shape[0])
countIteration = 0
file = open(out_fname, 'w')
listOfLoss = []

while diff and countIteration < 20:
    for i, pixel in enumerate(pixels):
        minDistance = float('inf')
        for j, centroid in enumerate(z):
            d = np.sqrt((centroid[0] - pixel[0]) ** 2 + (centroid[1] - pixel[1]) ** 2 + (centroid[2] - pixel[2]) ** 2)
            if d < minDistance:
                minDistance = d
                cluster[i] = j
    newCenter = findCenterCentroids(pixels, cluster, z).round(4)
    writeToFile(newCenter,file)
    listOfLoss.append(loss(pixels, cluster,newCenter))

    # if the old centroids is same like the new centroids - finish.
    if isEqual(z, newCenter):
        diff = 0
    else:
        z = newCenter
    countIteration += 1
# showGraph(listOfLoss)
file.close()









