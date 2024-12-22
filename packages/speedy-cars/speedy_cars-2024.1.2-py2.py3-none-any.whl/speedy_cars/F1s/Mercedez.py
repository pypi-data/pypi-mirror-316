# Python code to illustrate the Module 
class Mercedez: 
	# First we create a constructor for this class 
	# and add members to it, here models 
	def __init__(self): 
		self.models = ['a1','a2'] 

	# A normal print function 
	def outModels(self): 
		print('These are the available models for Mercedez') 
		for model in self.models: 
			print('\t%s ' % model) 
