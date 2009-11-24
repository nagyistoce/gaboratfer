#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ispis skupa značajki uzoraka za učenje u libsvm format.

import os
import sys
import test
import libsvmclassifier
import splitsamples

def printSample(features, label, dat):
	featuresStr = ""
	i = 0
	for f in features:
		i += 1
		featuresStr += " " + str(i) + ":" + str(f)
	
	print >>dat, str(label) + featuresStr

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uporaba: " + sys.argv[0] + " <putanja do direktorija s uzorcima> <izlazna datoteka>"
		sys.exit(-1)
	
	datOut = open(sys.argv[2], "w")

	# Slike za učenje se odabiru putem splitsample skripte.
	# Moguće ih je i predati preko stdin-a skripti (npr. ako
	# ste jednom odabrali slike i spremili popis u datoteku,
	# onda bi napraviti "cat uzorci.txt | ./printsamples.py <args...>")
	# Za takvo čitanje treba vam kod:
	#import sys
	#f = sys.stdin
	#while True:
		#line = f.readline()
		#if line == None or line == "": break
		#print "-- " + line
	
	path = sys.argv[1]
	(learning, testing) = splitsamples.splitit(path)
	if not path.endswith("/") and not path.endswith("\\"):
		is_win32 = (sys.platform == 'win32')
		if not is_win32: path += "/"
		else: path += "\\"

	for imgPath in learning:
		imgPath = path + imgPath
		lbl = int(imgPath[-11:-8])
		image = test.readImage(imgPath)
		features = libsvmclassifier.instance.extractFeatures(image)
		printSample(features, lbl, datOut)

	datOut.close()