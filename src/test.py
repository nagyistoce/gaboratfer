#!/usr/bin/env python

import Image
import sys, getopt, os
import gabor

import collector

# Put deciders here

import unclassifier

def main(argv):
	opts, args = getopt.getopt(argv, "", [])

	#for opt, arg in opts:	
	#	
	#
	filter = gabor.gaborFilter(5, 5, -1, -1, 1, 1, 5, 45, 0, 2, 0.5)

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
				file = open(inputImage, mode='rb')
				data = file.read()
				image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
				OMEGA[person].append(image)
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
