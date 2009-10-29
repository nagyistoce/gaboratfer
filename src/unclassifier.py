#!/usr/bin/env python

from classifier import Classifier
import Image
import random

class Unclassifier(Classifier):
	name = "Bles-o-mat"
	ids = []

	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		for x in traindata:
			for y in traindata[x]:
				# do stuff...
				pass
			self.ids.append(x)

	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		return random.choice(self.ids)


instance = Unclassifier()
