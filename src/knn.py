#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import Classifier
import Image
import random, math
import filterer

class GaborkNNclassifier(Classifier):
	name = "kNN sa gaborom"
	k = 3
	currentWorst = -1

	def distance(self, a, b):
		dist = 0
		for i in xrange(0, a.size):
			dist = dist + math.fabs(a[i] - b[i])*math.fabs(a[i] - b[i])
			if self.currentWorst != -1 and dist > self.currentWorst:
				return dist
		return dist
				
		

	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		tmp = traindata.values()[0][0]
		self.data = {}
		count = 0
		for x in traindata:		
			self.data[x] = []
			for y in traindata[x]:
				self.data[x].append(filterer.filterImage(y));
			count = count + 1
			if count % 10 == 0:
				print "Procesed %d classes" % (count)

	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		nn = []
		for x in xrange(0, self.k):
			nn.append([-1, -1])

		image = filterer.filterImage(image)

		self.currentWorst = -1
		for x in self.data:
			for y in self.data[x]:
				dist = self.distance(image, y)
				t = self.k - 1
				while t > -1 and (nn[t][0] == -1 or nn[t][0] > dist):
					if t < self.k - 1:
						nn[t + 1][0] = nn[t][0]
						nn[t + 1][1] = nn[t][1]
					nn[t][0] = dist
					nn[t][1] = x
				self.currentWorst = nn[self.k - 1][0]
		kNN = {}
		best = -1
		for x in xrange(0, self.k):
			if not nn[x][1] in kNN:
				kNN[nn[x][1]] = 0
			kNN[nn[x][1]] = kNN[nn[x][1]] + 1
			if best == -1 or kNN[nn[x][1]] > kNN[best]:
				best = nn[x][1]

		return best


instance = GaborkNNclassifier()
