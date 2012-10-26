"""
USStandardAtmosphere calculates atmospheric properties based on the 1975 model.

Note that this model differs slightly from the US standard atmospheric model. Go to wikipedia for more details.

ALL UNITS ARE SI BASE UNITS

Constructors:-

Implementation:-

"""

import math

class USStandardAtmosphere:

	#Constructors
	def __init__(self, alt=0, tOffset=0):
		self.altitude = alt
		self.temperature_offset = tOffset
		
		self.temperature = None
		self.pressure = None
		self.density = None
		self.speed_of_sound = None
		self.kinematic_viscosity = None
		
		self.makeEnvironment()
		self.base_layer = 'troposphere'
		self.gravity = 9.81

		#Private data for to define model
		__model_max_altitude = 87000
		__atmosphere_layers = {0:1, 11000:2, 20000:3, 32000:4, 47000:5, 51000:6, 71000:7}
		__layer_base_data = {
			0:{'temp':288.15, 'lapse':-0.0065, 'press':101325},
			1:{'temp':216.65, 'lapse':0.0, 'press':22632.1},
			2:{'temp':216.65, 'lapse':0.001, 'press':5474.89},
			3:{'temp':228.65, 'lapse':0.0028, 'press':868.019},
			4:{'temp':270.65, 'lapse':0.0, 'press':110.906},
			5:{'temp':270.65, 'lapse':-0.0028, 'press':66.9389},
			6:{'temp':214.65, 'lapse':-0.002, 'press':3.95642},
			}
		__gas_constant = 8.31432e3 
		__air_molar_mass = 0.0289644
		__specific_heat_ratio = 1.4
		__visc_lambda = 1.51204129
		__visc_sutherland_const = 120.0

	#Methods
	def makeEnvironment(self):
		if altitude > __model_max_altitude:
			raise ModelExtrapolationError
			
		for layer in __atmosphereLayer.keys():
			if altitude > layer:
				baselayer = __atmpsphere_layers[layer]
				base_alt = layer
		
		base_temp = __layer_base_data[base_layer]['temp']
		base_lapse = __layer_base_data[base_layer]['lapse']
		base_press = __layer_base_data[base_layer]['press']
		
		self.temperature = base_temp + self.altitude * base_lapse + self.temperature_offset
		
		if base-lapse == 0: 		
			self.pressure = base_press * math.exp((-1 * self.gravity * __air_molar_mass * (self.altitude - base_alt)) / (__gas_constant * base_temp))
		elif
			self.pressure = base_press * (base_temp / self.temperature) ** (self.gravity * __air_molar_mass / __gas_constant / base_lapse)

		self.density = __air_molar_mass * self.pressure / __gas_constant / self.temperature
		
		self.speed_of_sound = (__specific_heat_ratio * __gas_constant * self.temperature) ** 0.5
		
		self.kinematic_viscosity = __visc_lambda * self.temperature**(3/2) / (self.temperature + __visc_sutherland_const)

	def getEnvironment(self):
		enviro = {'alt':self.altitude, 'temp':self.temperature, 'dens':self.density, 'press':self.pressure, 
			'sos':self.speed_of_sound, 'kvisc':self.kinematic_viscosity}
		return enviro

	def getDynamicPressure(self, velocity):
		dynamic_press = 0.5 * self.density * velocity**2
		return dynamic_press

	def getReynoldsNumber(self, velocity, refLength):
		re_num = self.density * velocity * refLength / self.kinematic_viscosity
		return re_num

	def getMachNumber(self, velocity):
		ma_num = velocity / self.speed_of_sound
		return ma_num
		
	#Overloads
	def __str__(self):
		outString = 
		return outString

if __name__ == '__main__':
	bookTempSL = 288.16
	bookDensSL = 1.2250
	aa = USStandardAtmosphere()
	tempErrorSL = (aa.temperature - bookTempSL) / bookTempSL
	densErrorSL = (aa.density - bookDensSL) / bookDensSL
	
	bookTemp5K = 255.69
	bookDens5K = 7.6343e-1
	bb = USStandardAtmosphere(5000)
	tempError5K = (bb.temperature - bookTemp5K) / bookTemp5K
	densError5K = (bb.density - bookDens5K) / bookDens5K
	
	bookTemp20K = 216.66
	bookDens20K = 8.8909e-2
	cc = USStandardAtmosphere(20000)
	tempError20K = (cc.temperature - bookTemp20K) / bookTemp20K
	densError20K = (cc.density - bookDens20K) / bookDens20K

	
	bookTemp50K = 282.66
	bookDens50K = 1.0829e-3
	dd = USStandardAtmosphere(50000)
	tempError50K = (dd.temperature - bookTemp50K) / bookTemp50K
	densError50K = (dd.density - bookDens50K) / bookDens50K