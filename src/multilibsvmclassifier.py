from classifier import Classifier
import filterer
import math
import gabor
import libsvmclassifier

class Fil():
	def __init__(self, p, fs1, fs2):
		self.p = p
		self.fs1 = fs1
		self.fs2 = fs2
		
	def extract(self, image):
		return filterer.filterImageMultiParam(image, self.p, self.fs1, self.fs2)

# Samo u petlji stvarati filtere i instancirati klasifikator
lambdaSet = [2.5, 4, 5.6568, 8, 11.3137, 16]
orientationNum = 8
gamma = 0.5
bandwidth = math.pi
_filterSet1 = []
_filterSet2 = []
for Lambda in lambdaSet:
	for n in xrange(0, orientationNum):
		_filterSet1.append(gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, 0, bandwidth, gamma))
		_filterSet2.append(gabor.gaborFilterSimplified(Lambda, math.pi/8 * n, math.pi/2, bandwidth, gamma))


fil = Fil(8, _filterSet1, _filterSet2)
instance = libsvmclassifier.LibSVMclassifier(fil.extract)
instance.name = "libsvm-l:"+str(lambdaSet)+"-g:"+str(gamma)+"-b:"+str(bandwidth)+"-on:"+str(orientationNum)
