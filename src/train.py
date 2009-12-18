#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Treniranje klasifikatora i spremanje modela.

import Image
import sys, getopt, os
import collector

# Put decider here (Only first will be used, others will be ignored)
#import knn
import libsvmclassifier


clasifierImpl = collector.Collector.registered[0]
doSplit = False

def readImage(inputImage):
	file = open(inputImage, mode='rb')
	data = file.read()
	image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
	return image

def main(args, modelSavePath):
	trainData = {}
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
				if person not in trainData:
					trainData[person] = []
				trainData[person].append(readImage(inputImage))
				okCount = okCount + 1
			else:
				print "Skipping non-nrm file %s" % (inputImage)
		else:
			print "Skipping non-file %s" % (inputImage)
	
	print "Ukupno zadano %d razreda uzoraka." % (len(trainData))
	print "Ukupno zadano %d uzoraka." % (okCount)
	print
	
	if doSplit:
		for cls in trainData:
			trainData[cls] = trainData[cls][:-1]
	
	print "Training " + clasifierImpl.name + " classifier."
	
	clasifierImpl.train(trainData)
	clasifierImpl.saveModel(modelSavePath)
	
	print "Done!"
	print "Model for " + clasifierImpl.name + " classifier saved to: " + modelSavePath

def usage():
  print "Use: " + sys.argv[0] + " -m <modelSavePath> [--split] <images ...>"
  print "--split = Do data splitting (leavning last sample of each class for testing)"
  sys.exit(-1)

if __name__ == "__main__":
	args = sys.argv[1:]
	if "-m" in args:
		idx = args.index("-m")
		if len(args) <= idx+1:
			usage()
		modelSavePath = args[idx+1]
		args.remove("-m")
		args.remove(modelSavePath)
	else:
		usage()

	if "--split" in args:
		args.remove("--split")
		doSplit = True
	
	main(args, modelSavePath)