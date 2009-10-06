#!/usr/bin/env python

import Image
import sys, getopt
import gabor

def main(argv):
	opts, args = getopt.getopt(argv, "", [])

	#for opt, arg in opts:	
	#	
	#
	filter = gabor.gaborFilter(5, 5, -1, -1, 1, 1, 5, 45, 0, 2, 0.5)

	for inputImage in args:
		file = open(inputImage, mode='rb')
		data = file.read()
		image = Image.fromstring("L", (64, 64), data, "raw", "L", 0, 1)
		gaborific = gabor.apply(filter, image)
		gaborific.show()
	

if __name__ == "__main__":
	main(sys.argv[1:])
