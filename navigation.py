import math

"""location is a set of tools for handling 3D positions anywhere near a
planetary body in terms of body-fixed lattitude-longitude-altitude coordinates.
This package can also perform calculations on positions to give bearing and
range on great circles.

An important feature of this package is that it runs with only native python
libraries. Thus it can be made to run on anything that can run a basic python
environment without needing additional packages.

All units are metric

Extensive thanks to the individual behind http://www.movable-type.co.uk/ for
their awesome website detailing all this navigational stuff.
"""

#TODO: Add NMEA sentence support http://aprs.gids.nl/nmea/
#TODO: Add natural text input to handle DDoHH'MM'SS" support
#TODO: Add a framework to handle non-terran coordinates
#TODO: Add option to use eliptical geodetics

class Coordinates(object):
    """Coordinates objects handle instances of lattitude-longitude-altitude
    locations on and near a planetary body (near is an arbitrary term).

    This is a superclass that needs to be referenced to a planetary body to be
    useful in any way.
    """
    major_radius = None
    minor_radius = None
    average_radius = None

    def __init__(self, lat=0, lon=0, alt=0):
        self.Latitude = float(lat)
        self.Longitude = float(lon)
        self.Altitude = float(alt)

class TerranCoordinates(Coordinates):
    """TerranCoordinates defines locations on the earth using the WGS-84
    elipsoid model.
    """
    major_radius = 6378137.0
    minor_radius = 6356752.314245
    average_radius = (2.0*major_radius + minor_radius)/3.0

    def __init__(self, lat=0, lon=0, alt=0):
        Coordinates.__init__(self, lat, lon, alt)
        self.NMEA_dict = None

class AreanCoordinates(Coordinates)
    """AreanCoordinates defines locations on Mars using MOLA geodesy.
    http://tharsis.gsfc.nasa.gov/geodesy.html
    """
    major_radius = 3396200
    minor_radius = 3376189
    average_radius = 3389508

    def __init__(self, lat=0, lon=0, alt=0):
        Coordinates.__init__(self, lat, lon, alt)
        self.NMEA_dict = None

def get_surface_range(from_point, to_point):
    """Calculates the great circle range between two points using the haversine
    formula. This is the range across the surface of the geoid only, no
    altitude effects are included.
    """
    assert from_point.__class__ is to_point.__class__
    from_lat = math.radians(from_point.Latitude)
    from_lon = math.radians(from_point.Longitude)
    to_lat = math.radians(to_point.Latitude)
    to_lon = math.radians(to_point.Longitude)
    delta_lon = to_lon - from_lon
    delta_lat = to_lat - from_lat

    half_chord = math.sin(delta_lat/2.0)**2 + math.sin(delta_lon/2.0)**2 +
        math.cos(from_lat)*math.cos(to_lat)
    central_angle = 2.0 * math.atan2(math.sqrt(half_chord), math.sqrt(1-half_chord))
    surface_range = central_angle * from_point.average_radius

    return surface_range

def get_bearings(from_point, to_point):
    """get_bearings calculates inital and final bearing along the great cricle
    from one point to another.
    """
    assert from_point.__class__ is to_point.__class__
    from_lat = math.radians(from_point.Latitude)
    from_lon = math.radians(from_point.Longitude)
    to_lat = math.radians(to_point.Latitude)
    to_lon = math.radians(to_point.Longitude)
    delta_lon = to_lon - from_lon
    delta_lat = to_lat - from_lat

    a_initial = math.sin(delta_lon)*math.cos(to_lat)
    b_initial = math.cos(from_lat)*math.sin(to_lat) −
        math.sin(from_lat)*math.cos(to_lat)*math.cos(delta_lon)
    initial_bearing = math.atan2(a_initial,b_initial)

    a_final = math.sin(delta_lon)*math.cos(from_lat)
    b_final = math.cos(to_lat)*math.sin(from_lat) −
        math.sin(to_lat)*math.cos(from_lat)*math.cos(delta_lon)
    final_bearing = math.atan2(a_final,b_final)
    final_bearing = (final_bearing+180.0) % 360 #Reverses the bearing

    return (initial_bearing, final_bearing)

def get_end_point(from_point, distance, bearing, alt_change):
    """get_end_points calculates the location of a point a given distance and
    bearing away from an initial point. It returns a coordinate object for the
    end point.
    """
    from_lat = math.radians(from_point.Latitude)
    fron_lon = math.radians(from_point.Longitude)
    angular_distance = distance / from_point.average_radius

    end_lat = math.sin(from_lat)*math.cos(angular_distance) +
        math.cos(from_lat)*math.sin(angular_distance)*math.cos(bearing)
    end_lat = math.asin(end_lat)

    a = math.cos(from_lat)*math.sin(angular_distance)*math.sin(bearing)
    b = math.cos(angular_distance) - math.sin(from_lat)*math.sin(end_lat)
    end_lon = from_lon + math.atan2(a,b)

    end_alt = from_point.Altitude + alt_change

    end_point = from_point.__class__(end_lat, end_lon, end_alt)
    return end_point


def get_intersect_point(point1, bearing1, point2, bearing2):
    """get_intersect_point returns a coordinate object that is the intercept
    point for two vectors across a surface. This does not take into account the
    velocities along each vector.
    """
    from_lat = math.radians(from_point.Latitude)
    from_lon = math.radians(from_point.Longitude)
    to_lat = math.radians(to_point.Latitude)
    to_lon = math.radians(to_point.Longitude)
    delta_lon = to_lon - from_lon
    delta_lat = to_lat - from_lat

    cross_angle12 = 2*math.asin(math.sqrt(math.sin(delta_lat/2)**2 +
        math.cos(from_lat)*math.cos(to_lat)*math.sin(delta_lon/2)**2))

    bearing_a = math.acos(math.sin(to_lat) -
        math.sin(from_lat)*math.cos(from_lat)*math.cos(cross_angle12)/
        math.sin(cross_angle12))
    bearing_b = math.acos(math.sin(from_lat) -
        math.sin(to_lat)*math.cos(to_lat)*math.cos(cross_angle12)/
        math.sin(cross_angle12))

    if (math.sin(delta_lon)>0):
        bearing_12 = bearing_a
        bearing_21 = 2*math.pi - bearing_b
    else:
        bearing_12 = 2*math.pi - bearing_a
        bearing_21 = bearing_b


    
    #return intersect_point
    pass

def interpret_natural_string(input_string):
    ## DD = D + M/60 + S/3600
    pass

def interpret_nmea_sentence(input_string):
    pass

if __name__=="__main__":
    #The following two points are 357.3km apart.
    #Initial bearing 88.0844
    #Final bearing 91.9156
    a = TerranCoordinates(lat=50.0, lon=0.0, alt=0.0)
    b = TerranCoordinates(lat=50.0, lon=5.0, alt=0.0)
    rng = get_surface_range(a,b)
    brg = get_bearings(a,b)

    #A point 2000km due South (180) from point a is:
    # 32.0136N 0.0E
    c = get_end_point(a, 2e6, 180.0)

    #Points a,45 and b,315 intersect at:
    #51.5288N 2.5000E
    d = get_intersect_point(a, 45.0, b, 315.0)
