#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from numpy.fft import fft2, ifft2
import math
from PIL import Image
from scipy import signal

def gaborFunction(x, y, Lambda, theta, psi, sigma, gamma):
	"""	Gaborova funkcija.
		psi - faza kosinusa, u radijanima
		theta - orijentacija, u radijanima
	"""
	
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
	sigma = calcSigma(bandwidth, Lambda)
	filter = numpy.empty( (height, width) )
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
	image.save("filter.png")

def degToRad(deg):
	return 2 * math.pi * deg / 360.0

from scipy.stsci import convolve

def applyScipyConv(filter, image):
	r2 = image.size[0]
	c2 = image.size[1]
	r1 = len(filter)
	c1 = len(filter[0])
	image.shape = (r2, c2)
	image.dtype = numpy.uint8
	filter.shape = (r1, c1)
	result = signal.fftconvolve(image, filter)
	#result = signal.correlate(image, filter)
	#result = convolve.convolve2d(filter, image, fft=1)

	resultImage = Image.new("L", (r2, c2))
	resultCanvas = resultImage.load()
	valueMax = result.max()
	valueMin = result.min()
	
	for x in xrange(0, r2):
		for y in xrange(0, c2):
			resultCanvas[y, x] = (result[x, y] - valueMin) * 255 / (valueMax - valueMin)
	return resultImage

def apply(filter, image, MinPad=True, pad=True):
	""" Not so simple convolution """

	#Just for comfort:
	FFt = fft2
	iFFt = ifft2

	#The size of the images:
	r2 = image.size[0]
	c2 = image.size[1]
	r1 = len(filter)
	c1 = len(filter[0])
	
	#MinPad results simpler padding,smaller images:
	if MinPad:
		r = r1+r2
		c = c1+c2
	else:
		#if the Numerical Recipies says so:
		r = 2*max(r1,r2)
		c = 2*max(c1,c2)

	#For nice FFT, we need the power of 2:
	if pad:
		pr2 = int(math.log(r)/math.log(2.0) + 1.0 )
		pc2 = int(math.log(c)/math.log(2.0) + 1.0 )
		rOrig = r
		cOrig = c
		r = 2**pr2
		c = 2**pc2
	#end of if pad
	
	#numpy fft has the padding built in, which can save us some steps
	#here. The thing is the s(hape) parameter:
	fftimage = FFt(filter, s=(r,c))*FFt(image,s=(r,c))

	if pad:
		result = (iFFt(fftimage))[:rOrig,:cOrig].real
	else:
		result = (iFFt(fftimage)).real

	resultImage = Image.new("L", (r2, c2))
	resultCanvas = resultImage.load()
	valueMax = result.max()
	valueMin = result.min()
	
	for x in xrange(0, r2):
		for y in xrange(0, c2):
			resultCanvas[y, x] = (result[x, y] - valueMin) * 255 / (valueMax - valueMin)
	return resultImage

def applyDirectConvolution(filter, image):
	imageHeight = image.size[0]
	imageWidth = image.size[1]
	filterHeight = len(filter)
	filterWidth = len(filter[0])
	result = numpy.zeros ( (imageHeight, imageWidth) )
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
	def readImage(inputImage):
		file = open(inputImage, mode='rb')
		data = file.read()
		image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
		return image

	filtr = gaborFilter(8, 8, -4, -4, 4, 4, 2, 0, 0, 1, 1)

	img = readImage("./../data/000_2_1.nrm")
	#result = applyDirectConvolution(filtr, img)
	result = apply(filtr, img)
	#result = applyScipyConv(filtr, img)

	result.save("test.png")
