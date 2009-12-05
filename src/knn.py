#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import Classifier
import Image
import random, math
import gabor

class GaborkNNclassifier(Classifier):
	name = "kNN sa gaborom"
	k = 3
	currentWorst = -1
	leftBounds = []
	rightBounds = []

	def distance(self, a, b):
		dist = 0
		ac = a.load()
		bc = b.load()
		for i in xrange(0, a.size[0]):
			for j in xrange(self.leftBounds[i], self.rightBounds[i] + 1):
				dist = dist + math.fabs(ac[i, j] - bc[i, j])
				if self.currentWorst != -1 and dist > self.currentWorst:
					return dist
		return dist
				
		

	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		self.filter = gabor.gaborFilter(8, 8, -4, -4, 4, 4, 2, 0, 0, 1, 1)
		tmp = traindata.values()[0][0]
		tmpc = tmp.load()
		for i in xrange(0, tmp.size[0]):
			self.leftBounds.append(0)
			self.rightBounds.append(0)
			for j in xrange(0, tmp.size[1]):
				if tmpc[i, j] != 0:
					break
				self.leftBounds[i] = j
			for j in xrange(tmp.size[1] - 1, 0, -1):
				if tmpc[i, j] != 0:
					break
				self.rightBounds[i] = j
		self.data = {}
		count = 0
		for x in traindata:		
			self.data[x] = []
			for y in traindata[x]:
				self.data[x].append(gabor.apply(self.filter, y));
			count = count + 1
			if count % 10 == 0:
				print "Procesed %d classes" % (count)

	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		nn = []
		for x in xrange(0, self.k):
			nn.append([-1, -1])

		image = gabor.apply(self.filter, image)

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
