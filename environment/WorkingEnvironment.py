class WorkingEnvironment():
"""
WorkingEnvironment defines an abstract superclass for all working fluid environments.

"""

	#Instance variables set to strings
	altitude = 'empty'
	temperature = 'empty'
	density = 'empty'
	pressure = 'empty'
	speed_of_sound = 'empty'
	kinematic_viscosity = 'empty'
	
	def makeEnvironment(self):
		raise NotImplementedError
	
	def getEnvironment(self):
		enviro = {'alt':altitude, 'temp':temperature, 'dens':density, 'press':pressure, 
			'SoS':speed_of_sound, 'Kvisc':kinematic_viscosity}
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