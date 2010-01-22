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

# lambda je od 2 do 12 (pise da moze biti od 2 do 1/5 velicine slike)
# Orijentacije... pa samo broj varirati
# faza... mozda i tu samo broj varirati
# gamma >0 do 1

# Samo u petlji stvarati filtere i instancirati klasifikator
lambdaSets = [[2.5, 4, 5.6568, 8, 11.3137, 16], [2.5, 5, 10], [4, 8, 32]]
gammas = [0.5, 0.7, 1]
bandwidths = [0.5, 1.5, math.pi]
orientationNum = 8

for lambdaSet in lambdaSets:
	for gamma in gammas:
		for bandwidth in bandwidths:
			_filterSet1 = []
			_filterSet2 = []
			for Lambda in lambdaSet:
				for n in xrange(0, orientationNum):
					# gaborFilterSimplified(Lambda, theta, psi, bandwidth, gamma)
					_filterSet1.append(gabor.gaborFilterSimplified(Lambda, math.pi/orientationNum * n, 0, bandwidth, gamma))
					_filterSet2.append(gabor.gaborFilterSimplified(Lambda, math.pi/orientationNum * n, math.pi/2, bandwidth, gamma))

			fil = Fil(8, _filterSet1, _filterSet2)
			instance = libsvmclassifier.LibSVMclassifier(fil.extract)
			instance.name = "libsvm-l:"+str(lambdaSet)+"-g:"+str(gamma)+"-b:"+str(bandwidth)+"-on:"+str(orientationNum)

