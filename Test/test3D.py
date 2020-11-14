# -*- coding: utf-8 -*-
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = []
y = []
z = []
hu =[]

# Write contour points to file
with open("aviel2_grayscale.txt", "r") as inLines:
   for line in inLines.read().splitlines():
       curLine = line.split(',')
       x.append(float(curLine[0]))
       y.append(float(curLine[1]))
       z.append(float(curLine[2]))
       hu.append(int(curLine[3]))

# Convert to tuple
xdata = tuple(x)
ydata = tuple(y)
zdata = tuple(z)
color = tuple(hu)

ax = plt.axes(projection='3d')
ax.scatter3D(xdata, ydata, zdata, c=color, cmap='Greens');