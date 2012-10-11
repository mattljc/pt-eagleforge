class isoStandardAtmosphere(WorkingEnvironment)
"""
isoStandardAtmosphere calculates atmospheric properties based on the 1976 ISO model.

Note that this model differs slightly from the US standard atmospheric model. Go to wikipedia for more details.

ALL UNITS ARE SI BASE UNITS

Constructors:-
atm = isoStandardAtmosphere() <-- Defaults to sea level
atm = isoStandardAtmosphere(altitude)
atm = isoStandardAtmosphere(altitude, temperature offset)

Implementation:-

"""
	#Private data for to define model
	__model_max_altitude = 87000
	__atmosphere_layers = {0:'troposphere',31500:'stratosphere'}
	__layer_base_data = {
		'troposhere':{'temp':1, 'lapse':1, 'dens':1, 'press':1}
		'stratosphere':{'temp':1, 'lapse':1, 'dens':1, 'press':1}
		'thermosphere':{'temp':1, 'lapse':1, 'dens':1, 'press':1}
		'exosphere':{'temp':1, 'lapse':1, 'dens':1, 'press':1}
		}
	__gas_constant
	__visc_constants
	
	#Additional instance variables
	base_layer = 'troposphere'
	temperature_offset = 0
	
	#Constructors
	def __init__(self):
		self.altitude = 0
		self.makeEnvironment()
		
	def __init__(self, alt):
		self.altitude = alt
		self.makeEnvironment()
		
	def __init__(self, alt, tOffset):
		self.altitude = alt
		self.temperature_offset = tOffset
		self.makeEnvironment()
		
	#Methods
	def makeEnvironment(self)
		if altitude > __model_max_altitude
			raise ModelExtrapolationError
			
		for layer in __atmosphereLayer.keys()
			if altitude > layer
				base_layer = __atmpsphere_layers[layer]
		
		base_temp = __layer_base_data[base_layer]['temp']
		base_lapse = __layer_base_data[base_layer]['lapse']
		base_dens = __layer_base_data[base_layer]['dens']
		base_press = __layer_base_data[base_layer]['press']
		
		self.temperature = base_temp + self.altitude * base_lapse + self.temperature_offset
		
		self.density = 
		
		self.pressure =
		
		self.speed_of_sound =
		
		self.kinematic_viscosity =	
		