#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image
import sys, getopt, os

import collector

# Put deciders here

import knn
#import libsvmclassifier

def readImage(inputImage):
	file = open(inputImage, mode='rb')
	data = file.read()
	image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
	return image

def main(argv):
	opts, args = getopt.getopt(argv, "", [])

	OMEGA = {}
	okCount = 0

	for inputImage in args:
		if os.path.isfile(inputImage):
			fileName = os.path.split(inputImage)[1]
			extension = fileName.split('.')[-1]
			if extension == "nrm":
				ident = fileName.split('.')[0].split('_')
				person = ident[0]
				shot = ident[1]
				picture = ident[2]
				if person not in OMEGA:
					OMEGA[person] = []
				OMEGA[person].append(readImage(inputImage))
				okCount = okCount + 1
			else:
				print "Skipping non-nrm file %s" % (inputImage)
		else:
			print "Skipping non-file %s" % (inputImage)
	
	print "Ukupno zadano %d razreda uzoraka." % (len(OMEGA))
	print "Ukupno zadano %d uzoraka." % (okCount)
	print "Ukupno definirano %d klasifikatora." % (len(collector.Collector.registered))
	collector.Collector.printAll()

	trainData = {}
	for x in OMEGA:
		trainData[x] = OMEGA[x][:-1]
		
	collector.Collector.trainAll(trainData)

	print "Zavrsilo treniranje!"

	testData = {}
	for x in OMEGA:
		testData[x] = []
		testData[x].append(OMEGA[x][-1])

	collector.Collector.testAll(testData)

	print "Zavrsilo testiranje!"
	

if __name__ == "__main__":
	main(sys.argv[1:])
