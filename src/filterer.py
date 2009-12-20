#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gabor
import math
import numpy
from PIL import Image

filter = gabor.gaborFilterSimplified(2.5, 0, 0, 1, 1)
filters = []
for i in xrange(0,4):
	filters.append(gabor.gaborFilterSimplified(2.5, (math.pi/4.0)*i, 0, 1, 1))

# Promjena velicine slike
def stretch(im, size, filter=Image.NEAREST):
	im.load()
	im = im._new(im.im.stretch(size, filter))
	return im

# Kombiniranje filtera tako da se svi rezultati stave na jednu sliku
# veličine 128x128 (4 filtera), pa se slika downsamplea na 64x64.
# Jako loše...
def filterImageAppendedFilters(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))
		
	combined = Image.new("L", (128, 128))
	canvas = combined.load()
	
	for n in [0, 1]:
		leftFilter = filtered[n].load()
		rightFilter = filtered[n*2+1].load()
		for x in xrange(0,64):
			for y in xrange(0,64):
				canvas[x,y+64*n] = leftFilter[x,y]
				canvas[x+64,y+64*n] = rightFilter[x,y]

	combined = stretch(combined, (64,64))
	return combined

# Filtriranje slike preko više filtera (zasebno).
# Rezultati se spajaju odabirom najveće vrijednosti među svim
# rezultatima filtriranja.
# Ovo se još naziva L-inf norma.
def filterImageMultipassMaxNorm(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))

	combined = Image.new("L", (64, 64))
	canvas = combined.load()
	
	filteredCan = []
	for fil in filtered:
		filteredCan.append(fil.load())

	for x in xrange(0,64):
		for y in xrange(0,64):
			maxVal = -1
			for fc in filteredCan:
				if maxVal < fc[x,y]: maxVal = fc[x,y]
			
			canvas[x,y] = maxVal

	return combined

# Filtriranje slike preko više filtera (zasebno).
# Rezultati se spajaju odabirom najmanje vrijednosti među svim
# rezultatima filtriranja.
def filterImageMultipassMinVal(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))

	combined = Image.new("L", (64, 64))
	canvas = combined.load()
	
	filteredCan = []
	for fil in filtered:
		filteredCan.append(fil.load())

	for x in xrange(0,64):
		for y in xrange(0,64):
			minVal = -1
			for fc in filteredCan:
				if minVal == -1 or minVal > fc[x,y]: minVal = fc[x,y]
			
			canvas[x,y] = minVal

	return combined

# Filtriranje slike preko više filtera (zasebno).
# Rezultati se spajaju prosjekom vrijednosti među svim
# rezultatima filtriranja.
def filterImageMultipassAvg(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))

	combined = Image.new("L", (64, 64))
	canvas = combined.load()
	
	filteredCan = []
	for fil in filtered:
		filteredCan.append(fil.load())
	
	filtersNum = len(filteredCan)
	for x in xrange(0,64):
		for y in xrange(0,64):
			sum = 0
			for fc in filteredCan:
				sum += fc[x,y]
			
			canvas[x,y] = sum*1.0/filtersNum

	return combined

def filterImageMultiParam(image):
	
	lambdaSet = [2.5, 4, 5.6568, 8, 11.3137, 16]
	orientationNum = 8
	gamma = 0.5
	bandwidth = math.pi
	
	result = numpy.array([])
	
	for Lambda in lambdaSet:
		for n in xrange(0, orientationNum):
			f1 = gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, 0, bandwidth, gamma)
			f2 = gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, math.pi/2, bandwidth, gamma)
			r1 = gabor.applyConv(f1, image)
			r2 = gabor.applyConv(f2, image)
			
			# magnituda kompleksnog odziva filtra
			r = numpy.sqrt(r1*r1 + r2*r2)

			r = (r - r.min()) / (r.max() - r.min())
			
			r.shape = 4096,
			result = numpy.concatenate((result, r))
	
	
	return result
		 
def filterImage(image):
	# Kombinacija više filtera L-inf (max) normom
	return filterImageMultipassMaxNorm(image)

	# Čista slika
	#return image

	# Primjena samo jednog filtera
	#return gabor.apply(filter, image)

def extractFeatures(image):
	gabored = filterImage(image)
	imgvec = numpy.fromstring(gabored.tostring(), numpy.uint8)
	imgvec.shape = 1, 4096
	return imgvec[0]