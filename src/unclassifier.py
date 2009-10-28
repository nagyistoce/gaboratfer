#!/usr/bin/env python

from classifier import Classifier
import Image

class Unclassifier(Classifier):
	name = "Bles-o-mat"

	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		pass

	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		return 0


instance = Unclassifier()
