class ModelExtrapolationException(Exception):
	""" An exception to be raised when an operation requires data from outside
	a model's valid boundaries.
	"""
	pass
