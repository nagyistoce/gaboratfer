#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image
import sys, getopt, os, glob
import collector

# Klasifikacija s postojećim modelom.

# Put decider here (Only first will be used, others will be ignored)
#import knn
import libsvmclassifier


clasifierImpl = collector.Collector.registered[0]

def readImage(inputImage):
	file = open(inputImage, mode='rb')
	data = file.read()
	image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
	return image

def main(args):
	images = []

	if sys.platform == "win32":
		tmp = []
		for arg in args:
			if len(glob.glob(arg)) == 0:
				tmp += arg
			else:
				tmp += glob.glob(arg)
		args = tmp

	for inputImage in args:
		if os.path.isfile(inputImage):
			fileName = os.path.split(inputImage)[1]
			extension = fileName.split('.')[-1]
			if extension == "nrm":
				images.append((inputImage, readImage(inputImage)))
			else:
				print "Skipping non-nrm file %s" % (inputImage)
		else:
			print "Skipping non-file %s" % (inputImage)
	
	print "Ukupno zadano %d uzoraka." % (len(images))
	print
	
	print "Classifying by " + clasifierImpl.name + " classifier."

	for (name, img) in images:
		cls = clasifierImpl.classify(img)
		print name + " is classified as " + cls

def usage():
  print "Use: " + sys.argv[0] + " -m <modelPath> <images ...>"
  sys.exit(-1)

if __name__ == "__main__":
	args = sys.argv[1:]
	if "-m" in args:
		idx = args.index("-m")
		if len(args) <= idx+1:
			usage()
		modelPath = args[idx+1]
		args.remove("-m")
		args.remove(modelPath)
		try:
			clasifierImpl.loadModel(modelPath)
		except:
			print "Model " + modelPath + " doesn't exist!"
			usage()
	else:
		usage()

	main(args)