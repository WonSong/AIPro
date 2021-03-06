import json

class Model:
	def __init__(self, config, instance, messenger, preprocessor):
		assert messenger is not None
		assert preprocessor is not None
		if 'input_attribute' in config:
			self.input_attribute = config['input_attribute']
		if 'output_attribute' in config:
			self.output_attribute = config['output_attribute']
		
		self.model_fn = getattr(instance, config['method_name'])
		self.messenger = messenger
		self.preprocessor = preprocessor
		
	def run(self):
		self.messenger.start(self.process)

	def process(self, data):
		if hasattr(self, 'input_attribute'):
			if self.input_attribute in data:
				x = self.preprocessor.preprocess(data[self.input_attribute])
			else:
				x = None
		else:
			x = self.preprocessor.preprocess(data)
		
		# If there was an issue preprocessing (i.e. the JSON attribute was missing from the data), just discard this instance.
		if x is None:
			return

		if hasattr(self, 'output_attribute'):
			# Make sure we can add an output attribute :)
			if type(data) != dict:
				data = {'input_data': data}
			data[self.output_attribute] = self.model_fn(x)
		else:
			data = self.model_fn(x)
		if data:
			self.publish(data)

	def publish(self, data):
		self.messenger.publish(data)

	def stop(self):
		self.messenger.stop()
