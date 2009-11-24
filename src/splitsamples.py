#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import math
import random

testSamples = False
path = ""

def usage():
	print """Opcije:
	--path=<putanja do direktorija sa slikama> - OBAVEZNO zadati!
	--test - ispisuje popis test primjera umjesto primjera za ucenje
	-h --help
	"""

def processOptions():
	global path, testSamples

	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "path=", "test"])
		len(args) # Samo da se makne warning...
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	
	for o, a in opts:
		if o == "--path":
			path = a
		elif o == "--test":
			testSamples = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			print "Ne postoji parametar " + o + "!"
			usage()
			sys.exit(2)
	
	if path == "" or path == None:
	  usage()
	  sys.exit(2)

if __name__ == "__main__":
	processOptions()
	
	testing = []
	samples = os.listdir(path)
	samplesMap = {}
	for s in samples:
		if s.endswith(".nrm"):
			if s[0:3] in samplesMap.keys():
				samplesMap[s[0:3]].append(s)
			else:
				samplesMap[s[0:3]] = []
				samplesMap[s[0:3]].append(s)

	for k in samplesMap.keys():
		n = len(samplesMap[k])*0.2	# Za testiranje uzimamo 20% uzoraka
		if n < 1.0: n = 1
		else: n = math.floor(n)

		for i in range(0,int(n)):
			idx = random.randint(0, len(samplesMap[k])-1)
			testing.append(samplesMap[k].pop(idx))
	
	if testSamples:
		testing.sort()
		for ts in testing: print ts
	else:
		learning = []
		for lsl in samplesMap.values():
			learning.extend(lsl)
		learning.sort()
		for ls in learning: print ls
