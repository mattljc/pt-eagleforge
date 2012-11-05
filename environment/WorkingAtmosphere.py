"""
WorkingEnvironment defines a superclass for all working fluid environments.

This class initializes the minimum required atmospheric variables for the mission and physics simulators.
It also defines some helpful tools that make use of these essential variables.
At this level, the atmospheric model to be used does not favour one set of units over any other. 
"""
class WorkingAtmosphere:

	### CONSTRUCTOR	
	"""
	The constructor sets the desired altitude and initializes all data to None.	
	"""
	def __init__(self,alt=0):
		self.altitude = alt
		self.temperature = None
		self.density = None
		self.pressure = None
		self.speed_of_sound = None
		self.dynamic_viscosity = None
	
	### METHODS
	"""
	This method should populate the variables defined in the constructor, however it must be overloaded in a subclass that defines which model is to be used.
	"""
	def makeEnvironment(self):
		raise NotImplementedError("This method must be overloaded in a subclass to define the model to be used")

	def getDynamicPressure(self, velocity):
		dynamic_press = 0.5 * self.density * velocity**2
		return dynamic_press

	def getReynoldsNumber(self, velocity, refLength):
		re_num = self.density * velocity * refLength / self.dynamic_viscosity
		return re_num

	def getMachNumber(self, velocity):
		ma_num = velocity / self.speed_of_sound
		return ma_num

	### SYSTEM OVERLOADS
	


#Testing script for this module run as standalone
if __name__ == '__main__':
	a = WorkingEnvironment()
	print(a.altitude)
	print(a.temperature)

	b = WorkingEnvironment(1000)
	print(b.altitude)
	b.makeEnvironment()
