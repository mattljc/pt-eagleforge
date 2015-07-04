import numpy as np
import helpers.extra_exceptions
"""working_atmosphere defines the interface for any working environment for
vehicles that operate in a fluid.

This module also includes an implementation of the 1975 US Standard Atmosphere.
"""

class WorkingAtmosphere(object):
	"""
	WorkingEnvironment defines a superclass for all working fluid environments.

	This class initializes the minimum required atmospheric variables for the
	mission and physics simulators. It also defines some helpful tools that
	make use of these essential variables. At this level, the atmospheric model
	to be used does not favour one set of units over any other.
	"""

	def __init__(self,alt=0):
		self.Altitude = alt
		self.Temperature = None
		self.Density = None
		self.Pressure = None
		self.Speed_of_sound = None
		self.Dynamic_viscosity = None

	def make_atmosphere(self):
		"""make_atmosphere generates the parameters of the working fluid.
		"""
		raise NotImplementedError()

	def get_dynamic_pressure(self, velocity):
		"""get_dynamic_pressure returns the dynamic pressure at a given
		velocity in this environment.

		Be careful to ensure consistant units with the model in use.
		"""
		dynamic_press = 0.5 * self.density * velocity**2
		return dynamic_press

	def get_reynolds_number(self, velocity, refLength):
		"""get_reynolds_number returns the Reynolds number for a given flowise
		length and velocity in the specified environment.

		Be careful to ensure consistant units with the model in use.
		"""
		re_num = self.density * velocity * refLength / self.dynamic_viscosity
		return re_num

	def get_mach_number(self, velocity):
		"""get_mach_number returns the local Mach number for a given velocity
		in the specified environment.

		Be careful to ensure constant units with the model in use.
		"""
		ma_num = velocity / self.speed_of_sound
		return ma_num

	### SYSTEM OVERLOADS
	def __str__(self):
		# TODO: check the functionality of this string overload
		out = 'model class: %s \n' % (self.__class__.__name__)
		for key in self.__dict__.keys():
			out += ' %s = %s \n' % (key, self.__dict__[key])
		return out

class USStandardAtmosphere(WorkingAtmosphere):
	"""
	USStandardAtmosphere calculates atmospheric properties based on the 1975
	model, implemented using barometric formulae. See wikipedia for more
	details.

	ALL UNITS ARE SI BASE UNITS
	"""

	#Constructors
	def __init__(self, alt=0):
		"""
		Calls the superclass constructor to initialize the data, then constructs the model.
		Also accepts an optional temperature offset.
		"""
		WorkingAtmosphere.__init__(alt)
		#self.temperature_offset = tOffset
		self.temperature_offset = 0
		self.makeEnvironment()


	#Methods
	def makeEnvironment(self):
		"""
		Overloads the method in the superclass, defines the model using the barometric formulae and data from the model.
		"""
		base_layer = 0
		self.gravity = 9.81

		#Private data for to define model
		__model_max_altitude = 87000
		__atmosphere_layers = {0:0, 11000:1, 20000:2, 32000:3, 47000:4, 51000:5, 71000:6}
		__layer_base_data = {
			0:{'temp':288.15, 'lapse':-0.0065, 'press':101325},
			1:{'temp':216.65, 'lapse':0, 'press':22632.1},
			2:{'temp':216.65, 'lapse':0.001, 'press':5474.89},
			3:{'temp':228.65, 'lapse':0.0028, 'press':868.019},
			4:{'temp':270.65, 'lapse':0, 'press':110.906},
			5:{'temp':270.65, 'lapse':-0.0028, 'press':66.9389},
			6:{'temp':214.65, 'lapse':-0.002, 'press':3.95642},
			}
		__gas_constant = 8.31432#e3
		__air_molar_mass = 0.0289644
		__specific_heat_ratio = 1.4
		__visc_lambda = 1.51204129e-6
		__visc_sutherland_const = 120.0

		if self.altitude > __model_max_altitude:
			raise exceptions.ModelExtrapolationException('Maximum allowed altitude is %s m' %(__model_max_altitude))

		layerKeys = __atmosphere_layers.keys()
		layerKeys = list(layerKeys)
		layerKeys.sort()
		for layer in layerKeys:
			if self.altitude >= layer:
				base_layer = __atmosphere_layers[layer]
				base_alt = layer
		base_temp = __layer_base_data[base_layer]['temp']
		base_lapse = __layer_base_data[base_layer]['lapse']
		base_press = __layer_base_data[base_layer]['press']

		self.temperature = base_temp + base_lapse * (self.altitude - base_alt) + self.temperature_offset

		if base_lapse == 0:
			self.pressure = base_press * math.exp((-1 * self.gravity * __air_molar_mass * (self.altitude - base_alt)) / (__gas_constant * base_temp))
		else:
			self.pressure = base_press * (base_temp / self.temperature) ** (self.gravity * __air_molar_mass / __gas_constant / base_lapse)

		self.density = __air_molar_mass * self.pressure / __gas_constant / self.temperature

		self.speed_of_sound = (__specific_heat_ratio * __gas_constant * self.temperature / __air_molar_mass) ** 0.5

		self.dynamic_viscosity = __visc_lambda * self.temperature**(3/2) / (self.temperature + __visc_sutherland_const)

#Testing script
if __name__ == '__main__':

	a = WorkingAtmosphere(1000)
	a.makeEnvironment()
	print(a)

	print('\n\n')
	bookTempSL = 288.16
	bookDensSL = 1.2250
	aa = USStandardAtmosphere()
	tempErrorSL = (aa.temperature - bookTempSL) / bookTempSL
	densErrorSL = (aa.density - bookDensSL) / bookDensSL
	output = 'T = %s ... rho = %s' % (aa.temperature, aa.density)
	output += '\nSL: temp error = %.5f ... dens error = %.5f' % (tempErrorSL, densErrorSL)
	print(output)

	bookTemp5K = 255.69
	bookDens5K = 7.6343e-1
	bb = USStandardAtmosphere(5000)
	tempError5K = (bb.temperature - bookTemp5K) / bookTemp5K
	densError5K = (bb.density - bookDens5K) / bookDens5K
	output = 'T = %s ... rho = %s' % (bb.temperature, bb.density)
	output += '\n5K: temp error = %.5f ... dens error = %.5f' % (tempError5K, densError5K)
	print(output)

	bookTemp20K = 216.66
	bookDens20K = 8.8909e-2
	cc = USStandardAtmosphere(20000)
	tempError20K = (cc.temperature - bookTemp20K) / bookTemp20K
	densError20K = (cc.density - bookDens20K) / bookDens20K
	output = 'T = %s ... rho = %s' % (cc.temperature, cc.density)
	output += '\n20K: temp error = %.5f ... dens error = %.5f' % (tempError20K, densError20K)
	print(output)

	bookTemp50K = 270.65
	bookDens50K = 0.000978
	dd = USStandardAtmosphere(50000)
	tempError50K = (dd.temperature - bookTemp50K) / bookTemp50K
	densError50K = (dd.density - bookDens50K) / bookDens50K
	output = 'T = %s ... rho = %s' % (dd.temperature, dd.density)
	output += '\n50K: temp error = %s ... dens error = %s' % (tempError50K, densError50K)
	print(output)
	print(dd)

	ee = USStandardAtmosphere(1000000)
