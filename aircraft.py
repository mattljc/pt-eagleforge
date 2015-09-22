import numpy as np

from . import units
from . import quant

class Vehicle(object):
    """Vehicle is the super class for all aircraft types.

    Its not particularly useful on its own, but contains attributes and methods
    common to all aircraft types.
    """

    def __init__(self, component_list):
        """Constructor initializes a vehicle from a given list of components
        and calculates essential vehicle properties.
        """
        self.Components = component_list
        self.GrossMass = 0.0 * units.kilogram
        self.CenterOfGravity = np.matrix([0,0,0]).T * units.meter
        self.MomentOfInertia = np.matrix([[0,0,0],[0,0,0],[0,0,0]]) * units.kilogram * units.meter**3

    def get_gross_mass(self, mass_k_factor=1):
        """get_gross_mass calculates the total mass of the aircraft as the sum
        of component masses multiplied by and optional k-factor to account for
        inaccuracies in mass estimates (e.g glue weight). The k factor is also
        stored for reference.
        """
        self.KMass = mass_k_factor
        for thing in self.Components:
            self.GrossMass += thing.Mass.to(units.Kilogram)
        self.GrossMass = self.GrossMass * self.KMass
        self.GrossMass.to(units.kilogram)

    def get_center_of_gravity(self):
        """get_center_of_gravity calculates the center of gravity of the
        aircraft. See references for location of the coordinate origin.
        """
        for thing in self.Components:
            self.CenterOfGravity += thing.CenterOfGravity * thing.Mass
        self.CenterOfGravity = self.CenterOfGravity / self.GrossMass
        self.CenterOfGravity.to(units.meter)
