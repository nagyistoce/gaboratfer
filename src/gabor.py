#!/usr/bin/env python

from numpy import *
from PIL import Image

def gaborFunction(x, y, Lambda, theta, psi, sigma, gamma):
	cosTheta = math.cos(theta)
	sinTheta = math.sin(theta)
	xTheta = x * cosTheta  + y * sinTheta
	yTheta = -x * sinTheta + y * cosTheta
	e = math.exp( -(xTheta**2 + yTheta**2 * gamma**2) / (2 * sigma**2) )
	cos = math.cos( 2 * math.pi * xTheta / Lambda + psi )
	return e * cos

def gaborFilter(x, y, Lambda, theta, psi, sigma, gamma):
	filter = empty( (2 * x, 2 * y) )
	for i in range(-x, x):
		for j in range(-y, y):
			filter[i + x, j + y] = gaborFunction(i, j, Lambda, theta, psi, sigma, gamma)
	return filter

def gaborFilterImage(x, y, Lambda, theta, psi, sigma, gamma):
	filter = gaborFilter(x, y, Lambda, theta, psi, sigma, gamma)
	fmax = filter.max() 
	fmin = filter.min()
	image = Image.new("L", (2 * x - 1, 2 * y - 1))
	canvas = image.load()
	for i in range(1, 2 * x):
		for j in range(1, 2 * y):
			canvas[i - 1, j - 1] = (filter[i, j]  - fmin) * 255 / (fmax - fmin)

if __name__ == "__main__":
	gaborFilterImage(6, 6, 5, 45, 0, 2, 0.5)
			 
			
			
