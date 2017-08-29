'''
this is the base loader class
it will handle all the nitty gritty
of dealing with models, while
individual classes will just
'''

import gc
import abc

class SmappModel(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self, model_path):
		pass

	def delete(objs):
		'''
		deallocates the memory occupide by this model
		added as convinienve function to make ti easier
		to avoid running out of ram when working with
		several models at once, usage: delete(model1, model2)
		'''
		for obj in objs: del obj
		return gc.collect()

