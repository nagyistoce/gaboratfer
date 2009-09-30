#!/usr/bin/env python

import Image
import sys, getopt
import gabor

def main(argv):
	opts, args = getopt.getopt(argv, "", [])

	#for opt, arg in opts:	
	#	
	#

	for inputImage in args:
		file = open(inputImage, mode='rb')
		data = file.read()
		image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
		image.show()
	

if __name__ == "__main__":
	main(sys.argv[1:])
