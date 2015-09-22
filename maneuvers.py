import numpy as np

from . import units
from . import quant

"""maneuvers provides classes to build mission paths as a series of 'standard'
maneuvers and define actions along that course.

This module also contains several basic maneuvers for SLUF, level turns and
steady altitude changes.
"""

class Maneuver(object):
    """Maneuver is the superclass for all classes that define the motion of an
    aircraft. It defines an interface that the mission simulation classes make
    use of to determine aircraft performance.

    It is assumed that Maneuvers will be stored as a list in the mission sim,
    so no Maneuver list class or attributes are provided.
    """

    def __init__(self):
        """Nothing to do in this constructor.
        """
        pass

    def get_specific_energy(self):
        """get_specific_energy returns a value to be multiplied by the mass of
        the vehicle to give the energy required to perform the maneuver.
        """
        raise NotImplementedError

class SteadyLevel(Maneuver):
    """SteadyLevel indicates steady, level, unaccelerated flight (SLUF). This
    could be a cruise state where speed and altitude are constant as expected
    in the Breguet range equations.

    It assumes that it is receiving altitudes and velocities as pint objects.
    """

    def __init__(self, alt, vel, dist):
        """Constructor taking altitude and velocity as pint objects
        """
        self.Altitude = alt.to(units.meter)
        self.Veloctiy = vel.to(units.meter/units.second)
        self.LoadFactor = 1.0

    def get_specific_energy(self):
        """Returns the sum of the specific kinetic and gravitational energies.
        """
        ke = (self.Veloctiy ** 2) / 2
        pe = self.Altitude * 9.81*(units.meter/units.second**2)

        return (ke + pe).to(units.joule/units.kilogram)

class LevelTurn(Maneuver):
    """LevelTurn is a banked turn at constant speed and altitude.

    It assumes that it is receiving all its inputs as pint objects.
    """

    def __init__(self, radius, delta_hdg, alt, vel):
        self.Altitude = alt.to(units.meter)
        self.Veloctiy = vel.to(units.meter/units.second)
        self.TurnRadius = radius.to(units.meter)
        self.HeadingChange = delta_hdg.to(units.degrees)

        self.PathLength = 2 * np.pi * self.TurnRadius * self.HeadingChange.to(units.radians)
        self.LoadFactor = self.Velocity**2 / self.TurnRadius / 9.81*(units.meter/units.second**2)
        self.BankAngle = np.acos(1 / self.LoadFactor)

    def get_specific_energy(self):
        ke = (self.Veloctiy ** 2) / 2
        pe = self.Altitude * 9.81*(units.meter/units.second**2)

class AltitudeChange(Maneuver):
