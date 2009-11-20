#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classifier import Classifier
import Image, Numeric
import gabor
from svm import *

class LibSVMclassifier(Classifier):
	name = "libsvmclassifier"
	ids = []
	filter = gabor.gaborFilter(5, 5, -1, -1, 1, 1, 5, 45, 0, 2, 0.5)
	
	def train(self, traindata):
		""" 	Traindata sadrzi dictionary u kojem su kljucevi ID
			faca a vrijednosti liste Image objekata u kojima su slikice """
		
		self.ids = traindata.keys()[:]
		samples = []
		labels = []
		for k in self.ids:
			for s in traindata[k]:
				gabored = gabor.apply(filter, s)
				imgvec = Numeric.fromstring(gabored.tostring(), Numeric.UnsignedInt8)
				imgvec.shape = 1, 4096
				labels.append(k)
				samples.append(imgvec[0])
				
		problem = svm_problem(labels, samples)
		size = len(samples) # 4096
		param = svm_parameter(C = 10,nr_weight = 2,weight_label = [1,0],weight = [10,1])
		param.kernel_type = RBF;
		model = svm_model(problem,param)
		errors = 0
		for i in range(size):
			prediction = model.predict(samples[i])
			probability = model.predict_probability
			if (labels[i] != prediction):
				errors = errors + 1
		print "##########################################"
		print " kernel %s: error rate = %d / %d" % ("RBF", errors, size)
		print "##########################################"
		
		param = svm_parameter(kernel_type = RBF, C=10)
		model = svm_model(problem, param)
		print "##########################################"
		print " Decision values of predicting %s" % (samples[0])
		print "##########################################"
		
		print "Numer of Classes:", model.get_nr_class()
		d = model.predict_values(samples[0])
		for i in model.get_labels():
			for j in model.get_labels():
				if j>i:
					print "{%d, %d} = %9.5f" % (i, j, d[i,j])
					
		param = svm_parameter(kernel_type = RBF, C=10, probability = 1)
		model = svm_model(problem, param)
		pred_label, pred_probability = model.predict_probability(samples[1])
		print "##########################################"
		print " Probability estimate of predicting %s" % (samples[1])
		print "##########################################"
		print "predicted class: %d" % (pred_label)
		for i in model.get_labels():
			print "prob(label=%d) = %f" % (i, pred_probability[i])
		
	def classify(self, image):
		""" Image objekt, return mora biti tocan ID osobe """
		return self.ids[0]

instance = LibSVMclassifier()
