#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gabor
import math
from PIL import Image

filter = gabor.gaborFilter(8, 8, -4, -4, 4, 4, 2.5, 0, 0, 1, 1)
filters = []
for i in xrange(0,4):
	filters.append(gabor.gaborFilter(8, 8, -4, -4, 4, 4, 2.5, (math.pi/4.0)*i, 0, 1, 1))

# Promjena velicine slike
def stretch(im, size, filter=Image.NEAREST):
	im.load()
	im = im._new(im.im.stretch(size, filter))
	return im

# Ovo je losije i sporije...
def filterImageMultipass(image):
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

def filterImage(image):
	return gabor.apply(filter, image)

def extractFeatures(image):
	gabored = filterImage(image)
	imgvec = Numeric.fromstring(gabored.tostring(), Numeric.UnsignedInt8)
	imgvec.shape = 1, 4096
	return imgvec[0]
