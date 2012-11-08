"""
Contains the component superclass, along with superclasses for the five essential component types: propulsor, lifting surface, controller, body, payload.
"""

class Component:
	"""
	The base class of all things that are part of an aircraft, describing their essential properties.
	"""
	
	def __init__(self, name='unamed', mass=None, loc=None, cg_loc=None):
		"""
		Constructor for components, exact definitions of relative cg location must be given in subcomponent classes
		"""
		self.name = name
		self.mass = mass
		self.location = loc
		self.relative_cg_location = cg_loc

class Propulsor:
	"""
	The base class for all things that generate forces that translate an aircraft.
	"""
	pass

class LiftingSurface:
	"""
	The base class for all things that are intended to generate forces that counter the weight of an aircraft.
	"""
	pass

class Controller:
	"""
	The base class for all things that are intended to cause rotation of an aircraft about its axes.
	"""
	pass

class Payload:
	"""
	The bass class for all mission specific masses to be carried by an aircraft.
	"""
	pass

class Body:
	"""
	The base class for all parts of the aircraft that are intended to shield payloads and other equipment from the free stream. 
	"""
	pass
