import numpy as np
from . import units
from . import quant
import lift_models

"""component provides superclasses and interfaces for the fundamental component
types one might encounter on an aircraft.

Each of the fundamental types makes some fundamental assumption. Check that
these are correct for your purposes.
"""

class Component(object):
    """Component is the superclass for all components and contains the
    basic parameters that all physical components will have.
    """

    def __init__(self, name, mass, cg_loc, inertias):
        self.Name = name
        self.Mass = mass.to(units.kilogram)
        self.CGLocation = cg_loc.to(units.meter)
        self.Inertias = inertias.to(units.kilogram * units.meter**3)

class LiftingSurface(Componenet):
    """LiftingSurfaces generate aerodynamic lift to counteract the weigth of
    the vehicle.

    They are assumed to be aligned such that the lift force is perpendicular to
    the direction of travel.
    """

    def __init__(self, name, mass, cg_loc, inertias, lift_model, param_dict):
        assert isinstance(lift_model, lift_models.LiftModels)
        Component.__init__(self, name, mass, cg_loc, inertias)
        self.LiftModel = lift_model.__init__(param_dict)
        self.LiftModel.generate_lift_tables()

class Propulsor(Component):
    """Propulsors generate thrust along a given vector. This can be used to
    translate or rotate the vehicle.
    """

    def __init__(self, name, mass, cg_loc, inertias, prop_model, thrust_vector,
            param_dict):
        assert isinstance(prop_model, propulsion_models.PropulsionModels)
        Component.__init__(self, name, mass, cg_loc, inertias)
        self.PropModel = prop_model.__init__(param_dict)
        self.PropModel.generate_thrust_tables()

class DragBody(Component):
    """DragBody objects are anything that is exposed to the free-stream and
    only generates drag.
    """

    def __init__(self, name, mass, cg_loc, inertias, drag_model, param_dict):
        assert isinstance(drag_model, drag_models.DragModels)
        Component.__init__(self, name, mass, cg_loc, inertias)
        self.DragModel = drag_model.__init__(param_dict)
        self.DragModel.generate_drag_tables()
