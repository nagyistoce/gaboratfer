#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collector 

class Classifier:
	def __init__(self):
		collector.Collector.register(self)

	def loadModel(self, modelPath):
		raise Exception("Not implemented!")

	def saveModel(self, modelPath):
		raise Exception("Not implemented!")
