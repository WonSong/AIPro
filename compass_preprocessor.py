import traceback

class CompassPreprocessor:
	def __init__(self, config, instance):
		self.instance = instance
		self.preprocess_fn = self.default_preprocess
		if config and hasattr(instance, config['method_name']) and callable(getattr(instance, config['method_name'])):
			self.preprocess_fn = getattr(instance, config['method_name'])

	# If no preprocess function was provided, default to this one - just a wrapper to return the data itself 
	# (assuming if they don't want a preprocessor, the data is already OK)
	def default_preprocess(self, data):
		return data

	def preprocess(self, data):
		try:
			x = self.preprocess_fn(data)
			return x
		except Exception as e:
			print "Error during preprocessing:"
			print e
			traceback.print_exc()
			return None
