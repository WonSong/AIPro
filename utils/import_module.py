import imp
import os

def import_module_from_file(module_name, filename):
	try:
		if not os.path.isfile(filename):
			raise Exception("File does not exist: '%s'" % filename)
		else:
			module = imp.load_source(module_name, filename)
			return module
	except Exception as e:
		print("Module '%s' could not be loaded from file '%s'" % (module_name, filename))
		print(e)
		return None