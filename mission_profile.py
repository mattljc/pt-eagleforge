import numpy as np
import pint
import navigation as nav

"""mission_profile provides classes to build mission paths and define actions
along that course.
"""

class FlightPath(object):
    """Flightpath is the superclass for all mission path segments. It defines
    the start and end points for path segments and provides a minimum interface
    for maneuver classes inheriting FlightPath.
    """

    def __init__(self, start=(0.0, 0.0, 0.0), end=(0.0, 0.0, 0.0)):
        self.start = start
        self.end = end

    def calculate_heading(self):


    def calculate_distance(self):

    def calculate_endpoint(self):
        raise NotImplementedError()
