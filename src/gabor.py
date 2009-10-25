#!/usr/bin/env python

from numpy import *
from PIL import Image

def gaborFunction(x, y, Lambda, theta, psi, sigma, gamma):
	"""	Gaborova funkcija.
		psi - faza kosinusa, u stupnjevima
		theta - orijentacija, u stupnjevima
	"""
	
	# Pretvaram psi i theta u radijane
	psi = 2 * math.pi * psi/ 360
	theta = 2 * math.pi * theta/ 360
	
	cosTheta = math.cos(theta)
	sinTheta = math.sin(theta)
	xTheta = x * cosTheta  + y * sinTheta
	yTheta = -x * sinTheta + y * cosTheta
	e = math.exp( -(xTheta**2 + yTheta**2 * gamma**2) / (2 * sigma**2) )
	cos = math.cos( 2 * math.pi * xTheta / Lambda + psi )
	return e * cos

def calcSigma(bandwidth, Lambda):
	return (Lambda / math.pi) * math.sqrt(math.log(2, math.e)/2)*(2**bandwidth + 1)/(2**bandwidth - 1)
	
def gaborFilter(height, width, minx, miny, maxx, maxy, Lambda, theta, psi, bandwidth, gamma):
	"""	Gaborov filter.
		psi - faza kosinusa, u stupnjevima
		theta - orijentacija, u stupnjevima
	"""
	
	sigma = calcSigma(bandwidth, Lambda)
	filter = empty( (height, width) )
	xFactor = 1.0 * (maxx - minx) / height
	yFactor = 1.0 * (maxy - miny) / width
	for i in xrange(0, height):
		for j in xrange(0, width):
			filter[i, j] = gaborFunction(minx + i * xFactor, miny + j * yFactor, Lambda, theta, psi, sigma, gamma)
	return filter

def gaborFilterImage(height, width, minx, miny, maxx, maxy, Lambda, theta, psi, bandwidth, gamma):
	filter = gaborFilter(height, width, minx, miny, maxx, maxy, Lambda, theta, psi, bandwidth, gamma)
	fmax = filter.max() 
	fmin = filter.min()
	image = Image.new("L", (height, width))
	canvas = image.load()
	for i in xrange(0, height):
		for j in xrange(0, width):
			canvas[i, j] = (filter[i, j]  - fmin) * 255 / (fmax - fmin)
	image.show()

def apply(filter, image):
	imageHeight = image.size[0]
	imageWidth = image.size[1]
	filterHeight = len(filter)
	filterWidth = len(filter[0])
	result = zeros ( (imageHeight, imageWidth) )
	imageCanvas = image.load()
	for x in xrange(0, imageHeight):
		for y in xrange(0, imageWidth):
			for i in xrange(0, filterHeight):
				for j in xrange(0, filterWidth):
					imageValue = 0
					xTrans = x - filterHeight / 2 + i
					yTrans = y - filterWidth / 2 + i
					if xTrans >= 0 and xTrans < imageHeight:
						if yTrans >= 0 and yTrans < imageWidth:
							imageValue = imageCanvas[xTrans, yTrans]					
					result[x, y] += filter[i, j] * imageValue
	resultImage = Image.new("L", (imageHeight, imageWidth))
	resultCanvas = resultImage.load()
	valueMax = result.max()
	valueMin = result.min()
	for x in xrange(0, imageHeight):
		for y in xrange(0, imageWidth):
			resultCanvas[x, y] = (result[x, y] - valueMin) * 255 / (valueMax - valueMin)
	return resultImage

if __name__ == "__main__":
	#gaborFilterImage(320, 320, -6, -6, 6, 6, 5, 90, 0, 2, 0.5)
	gaborFilterImage(100, 100, -50, -50, 50, 50, 10, 0, 0, 1, 0.5)
	
