#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import Classifier
import Image, Numeric
import gabor
from svm import *

class LibSVMclassifier(Classifier):
	name = "libsvmclassifier"
	ids = []
	model = None
	
	def __init__(self):
		filter = gabor.gaborFilter(5, 5, -1, -1, 1, 1, 5, 45, 0, 2, 0.5)
	
	def extractFeatures(self, image):
		global filter
		gabored = gabor.apply(filter, image)
		imgvec = Numeric.fromstring(gabored.tostring(), Numeric.UnsignedInt8)
		imgvec.shape = 1, 4096
		sampleVector = []
		for sample in imgvec[0]:
			sampleVector.append(float(sample)/255.0)	# Skaliranje! [0,1]
		return sampleVector

	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		global model
		
		svmc.svm_set_quiet()
		
		self.ids = traindata.keys()[:]
		samples = []
		labels = []
		for k in self.ids:
			for s in traindata[k]:
				currSample = extractFeatures(s)
				labels.append(float(k))
				samples.append(currSample)
				
		problem = svm_problem(labels, samples)
		size = len(samples) # 4096
		param = svm_parameter(C = 10,nr_weight = 2,weight_label = [1,0],weight = [10,1])
		param.kernel_type = RBF;
		model = svm_model(problem,param)
		# TODO: Spremi model u datoteku: model.save('svmmodel.model')
		# Ucitavanje iz datoteke: m = svm_model('svmmodel.model')
		
		#errors = 0
		#for i in range(size):
			#prediction = model.predict(samples[i])
			#probability = model.predict_probability
			#if (labels[i] != prediction):
				#errors = errors + 1
		#print "##########################################"
		#print " kernel %s: error rate = %d / %d" % ("RBF", errors, size)
		#print "##########################################"
		
	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		global model
		
		if model == None: return -1
		else:
			currSample = extractFeatures(image)
			return model.predict(currSample)

instance = LibSVMclassifier()
