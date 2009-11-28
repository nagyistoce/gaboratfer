# -*- coding: utf-8 -*-
# DON'T. EVEN. TRY.

class Collector:
	registered = []

	def __call__(self):
		return self

	def register(self, classifier):
		self.registered.append(classifier)

	def printAll(self):
		for i in self.registered:
			print "Klasifikator: %s" % (i.name)
	
	def trainAll(self, trainData):
		for i in self.registered:
			print "Treniram klasifikator: %s" % (i.name)
			i.train(trainData)

	def testAll(self, testData):
		for i in self.registered:
			print "Testiram klasifikator: %s" % (i.name)
			totalCount = 0
			correctCount = 0
			for x in testData:
				for z in testData[x]:
					totalCount = totalCount + 1
					if i.classify(z) == x:
						correctCount = correctCount + 1
					if totalCount % 10 == 0:
						print "Ispitano %d uzoraka (%d : %d rezultat)" % (totalCount, correctCount, totalCount - correctCount)
			print "%s je tocno klasificirao %d od %d uzoraka (%f posto)" % (i.name, correctCount, totalCount, correctCount * 100.0 / totalCount)
			

Collector = Collector()

