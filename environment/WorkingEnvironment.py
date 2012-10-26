"""
WorkingEnvironment defines a superclass for all working fluid environments.
"""
class WorkingEnvironment:
	
	"""
	The constructor sets the desired altitude and initializes all data to None.	
	"""
	def __init__(self,alt=0):
		self.altitude = alt
		self.temperature = None
		self.density = None
		self.pressure = None
		self.speed_of_sound = None
		self.kinematic_viscosity = None
	
	def makeEnvironment(self):
		raise NotImplementedError("This method must be overloaded in a subclass to define the model to be used")
	
	def getEnvironment(self):
		enviro = {'alt':altitude, 'temp':temperature, 'dens':density, 'press':pressure, 
			'sos':speed_of_sound, 'kvisc':kinematic_viscosity}
		return enviro
		
	def getDynamicPressure(self, velocity):
		dynamic_press = 0.5 * density * velocity**2
		return dynamic_press
		
	def getReynoldsNumber(self, velocity, surfaceLength):
		re_num = density * velocity * surfaceLength / kinematic_viscosity
		return re_num
	
	def getMachNumber(self, velocity):
		ma_num = velocity / speed_of_sound
		return ma_num

#Testing script for this module run as standalone
if __name__ == '__main__':
	a = WorkingEnvironment()
	print(a.altitude)
	print(a.temperature)

	b = WorkingEnvironment(1000)
	print(b.altitude)
	b.makeEnvironment()
