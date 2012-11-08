
class WorkingAtmosphere:
	"""
	WorkingEnvironment defines a superclass for all working fluid environments.

	This class initializes the minimum required atmospheric variables for the mission and physics simulators.
	It also defines some helpful tools that make use of these essential variables.
	At this level, the atmospheric model to be used does not favour one set of units over any other. 
	"""

	### CONSTRUCTOR	

	def __init__(self,alt=0):
		"""
		The constructor sets the desired altitude and initializes all data to None.	
		"""
		self.altitude = alt
		self.temperature = None
		self.density = None
		self.pressure = None
		self.speed_of_sound = None
		self.dynamic_viscosity = None
	
	### METHODS
	def makeEnvironment(self):
		"""
		This method should populate the variables defined in the constructor. It must be overloaded in a subclass that defines which model is to be used.
		"""
		raise NotImplementedError("This method must be overloaded in a subclass to define the model to be used")

	def getDynamicPressure(self, velocity):
		"""
		Returns the dynamic pressure at a given velocity in the specified environment.
		Be careful to ensure consistant units with the model in use.
		"""
		dynamic_press = 0.5 * self.density * velocity**2
		return dynamic_press

	def getReynoldsNumber(self, velocity, refLength):
		"""
		Returns the Reynolds number for a given flowise length and velocity in the specified environment.
		Be careful to ensure consistant units with the model in use.
		"""
		re_num = self.density * velocity * refLength / self.dynamic_viscosity
		return re_num

	def getMachNumber(self, velocity):
		"""
		Returns the local Mach number for a given velocity in the specified environment.
		Be careful to ensure constant units with the model in use. 
		"""
		ma_num = velocity / self.speed_of_sound
		return ma_num

	### SYSTEM OVERLOADS
	def __str__(self):
		out = 'model class: %s \n' % (self.__class__.__name__)
		for key in self.__dict__.keys():
			out += ' %s = %s \n' % (key, self.__dict__[key])
		return out
	


#Testing script for this module run as standalone
if __name__ == '__main__':
	a = WorkingAtmosphere()
	print(a)

	b = WorkingAtmosphere(1000)
	print('\n'+b)
	b.makeEnvironment()
