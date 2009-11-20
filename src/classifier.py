#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collector 

class Classifier:
	def __init__(self):
		collector.Collector.register(self)
