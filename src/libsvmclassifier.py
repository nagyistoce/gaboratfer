#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import Classifier
import os
import filterer
from svm import *

class LibSVMclassifier(Classifier):
	name = "libsvmclassifier"
	ids = []
	model = None
	
	def extractFeatures(self, image):
		imgvec = filterer.extractFeatures(image)
		sampleVector = []
		for sample in imgvec:
			sampleVector.append(float(sample))	# Skaliranje! [0,1]
		return sampleVector
	
	def loadModel(self, modelPath):
		if not os.path.isfile(modelPath): raise Exception("Model doesn't exist: " + modelPath)
		self.model = svm_model(modelPath)
	
	def saveModel(self, modelPath):
		if self.model == None: raise Exception("No model set!")
		self.model.save(modelPath)
		
	def train(self, traindata):
		""" Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		
		svmc.svm_set_quiet()
		
		self.ids = traindata.keys()[:]
		samples = []
		labels = []
		for k in self.ids:
			for s in traindata[k]:
				currSample = self.extractFeatures(s)
				labels.append(float(k))
				samples.append(currSample)

		problem = svm_problem(labels, samples)
		param = svm_parameter(kernel_type = RBF, C = 2**12, gamma = 2**-11)
		self.model = svm_model(problem, param)
		
	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		
		if self.model == None: raise Exception("No model set!")
		else:
			currSample = self.extractFeatures(image)
			cls = self.model.predict(currSample)
			return "%03.0f" % cls

instance = LibSVMclassifier()
