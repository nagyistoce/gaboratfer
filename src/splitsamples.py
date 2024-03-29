#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dijeljenje skupa uzoraka na skup za testiranje i skup za učenje.
# Podjela ide slučajnim odabirom 20% uzoraka u skup za testiranje.
# Skup za učenje se ispisuje na stdout, a ako je stavljena zastavica --test
# onda se ispisuje skup za testiranje.

# Ovo neka se ne koristi jer nema previše smisla... 20% pojedinog razreda je u većini slučajeva između 0 i 2.
# Podjela na uzorke već postoji u test.py (zadnji uzorak se uzima za testiranje).
# Ovo se eventualno može prilagoditi radi printsamples.py radi određivanja parametara preko grid.py

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

def splitit(path):
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
	
	testing.sort()
	learning = []
	for lsl in samplesMap.values():
		learning.extend(lsl)
	learning.sort()
	return (learning, testing)

if __name__ == "__main__":
	processOptions()
	
	(learning, testing) = splitit(path)
	
	if testSamples:
		for ts in testing: print ts
	else:
		for ls in learning: print ls
