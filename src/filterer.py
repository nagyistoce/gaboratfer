#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gabor

filter = gabor.gaborFilter(8, 8, -4, -4, 4, 4, 2, 0, 0, 1, 1)

def filterImage(image):
	return gabor.apply(filter, image)

def extractFeatures(image):
	gabored = filterImage(image)
	imgvec = Numeric.fromstring(gabored.tostring(), Numeric.UnsignedInt8)
	imgvec.shape = 1, 4096
	return imgvec[0]
