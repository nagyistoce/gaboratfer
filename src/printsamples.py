#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ispis skupa značajki uzoraka za učenje u libsvm format.

import os
import sys
import test
import libsvmclassifier

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uporaba: " + sys.argv[0] + " <putanja do direktorija s uzorcima> <izlazna datoteka>"
		sys.exit(-1)
	
	# Sad treba skužiti kako pročitati sve što se pipe-a na skriptu.
	# Sve pipeano pročitati, pozvati drugu skriptu koja će to obraditi (preko importa)
	# i te podatke zapisati u libsvm format u izlaznu datoteku
	
	# @Test
	image = test.readImage("/media/Work/gabor/face/000_1_1.nrm")
	libsvmc = libsvmclassifier.LibSVMclassifier()
	print libsvmc.extractFeatures(image)