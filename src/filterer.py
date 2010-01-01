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

	canvas = numpy.ones(image.shape)
	
	for x in xrange(0,image.shape[0]):
		for y in xrange(0,image.shape[1]):
			maxVal = -1
			for fc in filtered:
				if maxVal < fc[x,y]: maxVal = fc[x,y]
			
			canvas[x,y] = maxVal

	return canvas

# Filtriranje slike preko više filtera (zasebno).
# Rezultati se spajaju odabirom najmanje vrijednosti među svim
# rezultatima filtriranja.
def filterImageMultipassMinVal(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))

	canvas = numpy.ones((64, 64))

	for x in xrange(0,64):
		for y in xrange(0,64):
			maxVal = -1
			for fc in filtered:
				if minVal == -1 or minVal > fc[x,y]: minVal = fc[x,y]
			
			canvas[x,y] = minVal

	return canvas

# Filtriranje slike preko više filtera (zasebno).
# Rezultati se spajaju prosjekom vrijednosti među svim
# rezultatima filtriranja.
def filterImageMultipassAvg(image):
	filtered = []
	for filtr in filters:
		filtered.append(gabor.apply(filtr, image))

	canvas = numpy.ones((64, 64))
	
	filtersNum = len(filtered)
	for x in xrange(0,64):
		for y in xrange(0,64):
			sum = 0
			for fc in filtered:
				sum += fc[x,y]
			
			canvas[x,y] = sum*1.0/filtersNum

	return combined

# Filteri i parametri potrebni filterImageMultiParam() filtriranju
lambdaSet = [2.5, 4, 5.6568, 8, 11.3137, 16]
orientationNum = 8
gamma = 0.5
bandwidth = math.pi
filterSet1 = []
filterSet2 = []
filtersNum = 0
for Lambda in lambdaSet:
	for n in xrange(0, orientationNum):
		filterSet1.append(gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, 0, bandwidth, gamma))
		filterSet2.append(gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, math.pi/2, bandwidth, gamma))
		filtersNum += 1
#downsampling faktor
p =  8

def filterImageMultiParam(image):
	result = numpy.array([])

	for n in xrange(0, filtersNum):
		f1 = filterSet1[n]
		f2 = filterSet2[n]
		r1 = gabor.apply(f1, image)
		r2 = gabor.apply(f2, image)
		
		# magnituda kompleksnog odziva filtra
		r = numpy.sqrt(r1*r1 + r2*r2)
		
		#downsampling
		rc,cc = r.shape
		r.shape = (rc*cc/p, p)
		r = r.sum(1)
		r.shape = (rc/p, p, cc/p)
		r = r.sum(1)/(p*p) 
		
		r = (r - r.min()) / (r.max()-r.min())

		result = numpy.concatenate((result,r.ravel()))
	
	return result
		 
def filterImage(image):
	# Kombinacija više filtera L-inf (max) normom
	# return filterImageMultipassMaxNorm(image)

	return filterImageMultiParam(image)

	# Čista slika
	#return numpy.asarray(image)

	# Primjena samo jednog filtera
	#return gabor.apply(filter, image)

def extractFeatures(image):
	gabored = filterImage(image)
	return gabored.ravel()