import numpy as np
from scipy.spatial.transform import Rotation as R
import typing
import pytz
import time
from tzwhere import tzwhere
import math
from datetime import datetime

tzWhere = tzwhere.tzwhere(forceTZ=True)


def Calc3DEnergy(length: float, width: float, inclination: float, orientation: float, efficiency: float, latitude: float, longitude: float, dates: typing.List[datetime], weather: typing.List[float]) -> typing.List[float]:
    # length, width in meters
    # inclination in degrees, 0° is flat, 90° is standing
    # orientation in degrees, 0° is north, 90° is east
    # latitude in degrees, +N
    # longitude in degrees, +E

    orientation = orientation - 90

    output = []

    # 1st step : compute sun's position in the sky
    fst_start = time.perf_counter()

    tzName = tzWhere.tzNameAt(latitude, longitude, forceTZ=True)
    timezone = pytz.timezone(tzName)
    
    timeDelta = timezone.utcoffset(dates[0])
    utc_dates = [d + timeDelta for d in dates]
    sun_positions = np.array([sunpos(
        (d.year, d.month, d.day, d.hour, 0, 0, 0), (latitude, longitude)) for d in utc_dates])
    sun_altitudes = sun_positions[:, 0]
    sun_altitudes[sun_altitudes < 0] = 0
    sun_azimuths = sun_positions[:, 1]

    # Convert in radians
    # +x is east
    # +y is north
    # +z is up
    sun_altitudes = np.radians(np.array(sun_altitudes))
    sun_azimuths = np.radians(np.array(sun_azimuths))

    # 2nd step : compute solar panel's shadow for each sun position
    snd_start = time.perf_counter()
    # +x is east
    # +y is north
    # +z is up
    # convert angles in radians
    rad_incl = np.radians(inclination)
    rad_orient = np.radians(orientation)

    rot_incl = R.from_euler('x', rad_incl, degrees=False)
    rot_orient = R.from_euler('z', rad_orient, degrees=False)

    full_rot: np.ndarray = rot_orient.as_matrix().dot(rot_incl.as_matrix())

    # Draw the shape on the floor then apply rotations:
    
    other_base_vertex = full_rot.dot(np.array([width, 0, 0]))

    top_vertex = full_rot.dot(np.array([0, length, 0]))

    # 3rd step : cast shadow of shape on the floor
    trd_start = time.perf_counter()
    x_coeffs = np.cos(sun_azimuths)
    y_coeffs = np.sin(sun_azimuths)
    z_coeffs = np.sin(sun_altitudes)

    t_other_base_values = np.divide(-other_base_vertex[2], z_coeffs)
    t_top_values = np.divide(-top_vertex[2], z_coeffs)

    
    other_base_vertex_projs = np.transpose(np.array([np.multiply(x_coeffs, t_other_base_values), np.multiply(
        y_coeffs, t_other_base_values), np.zeros(len(t_other_base_values))]))
    other_base_vertex_projs += other_base_vertex
    
    other_base_vertex_projs = other_base_vertex_projs[:,:2]
    
    top_vertex_projs = np.transpose(np.array([np.multiply(x_coeffs, t_top_values), np.multiply(
        y_coeffs, t_top_values), np.zeros(len(t_top_values))]))
    top_vertex_projs += top_vertex
    top_vertex_projs = top_vertex_projs[:,:2]
    

    # 4th step : compute and orient shadows
    fourth_start = time.perf_counter()
    # Compute vector product to orient shape; results should have same orientation
    ref_orientation = np.sign(np.cross(other_base_vertex, top_vertex)[2])
    other_orientations = np.sign(
        np.cross(other_base_vertex_projs, top_vertex_projs))
    well_oriented = np.multiply(
        other_orientations, other_orientations == ref_orientation)
    
    stacks = np.stack([other_base_vertex_projs,top_vertex_projs],1)
    
    #areas = np.array([np.linalg.det(s) for s in stacks])
    areas = np.linalg.det(stacks)
    areas = np.multiply(areas, well_oriented)
    areas[np.isnan(areas)] = 0
    areas = np.abs(areas)
    

    # 5th step : convert to energy
    fifth_start = time.perf_counter()
    output = np.multiply(areas, weather)*efficiency

    stop_time = time.perf_counter()

    #print(f"1st section: {snd_start - fst_start}\n2nd section: {trd_start-snd_start}\n3rd section: {fourth_start-trd_start}\n4th section: {fifth_start-fourth_start}\n5th section: {stop_time-fifth_start}")

    return output


def CalcEnergy(L, l, alpha, beta, eta, lat, weather):
    # Inputs :
    # L : length of solar panels
    # l : width
    # alpha : inclination angle in °, 0 flat on ground 90° standing
    # beta : orientation towards south, 0° full South, 90° East
    # eta : efficiency of panel [0;1]
    # lat : latitude of building
    # weather : solar radiation energy per hour in a year [Wh/m^2]

    alpha = (90-alpha) * np.pi / 180
    beta = beta * np.pi / 180

    phi = lat / 180 * np.pi

    day = np.arange(0, 365)
    deltas = 23.45 * np.sin(2 * np.pi * ((day - 81) / 365)) / 180 * np.pi
    hour = np.arange(0, 24)
    h = np.zeros(0)
    a = h
    for i in day:
        hd = np.arcsin(np.sin(
            phi)*np.sin(deltas[i])+np.cos(phi)*np.cos(deltas[i])*np.cos(15*(hour-12)/180 * np.pi))
        h = np.append(h, hd)
        had = np.arcsin(np.sin(
            phi) * np.sin(-deltas[i])+np.cos(phi)*np.cos(deltas[i])*np.cos(15*(hour-12)/180*np.pi))
        ad = np.arcsin(np.cos(deltas[i]) / np.cos(had)
                       * np.sin(15 * (hour - 12) / 180 * np.pi))
        a = np.append(a, ad)

    # Set the night values to 0
    h = np.clip(h, 0, None)

    for i in range(len(a)):
        if i == len(a) - 1:
            a[i] = np.pi / 2
        elif a[i] > a[i + 1]:
            a[i] = np.pi / 2

    # Solar panel shadow calculation
    hp = l * np.sin(alpha) + l * np.cos(alpha) * np.tan(h)
    Lp = L * np.sin(beta + np.pi / 2 - a)

    s = np.clip(np.multiply(hp, Lp), 0, None)
    # Energy produced
    e = np.multiply(s, weather) * eta

    return e


def sunpos(when, location):
    # Extract the passed data
    year, month, day, hour, minute, second, timezone = when
    latitude, longitude = location
    # Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2
    # Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude)
    # Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second / \
        3600  # Days from J2000, accurate from 1901 to 2099
    daynum = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        - 730531.5
        + greenwichtime / 24
    )  # Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873  # Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768  # Ecliptic longitude of the sun
    eclip_long = (
        mean_long
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
    )
    # Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * \
        daynum

    # Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long),
                 cos(eclip_long))
    # Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))
    # Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon
    # Hour angle of the sun
    hour_ang = sidereal - rasc
    # Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat)
                     * cos(hour_ang))
    # Local azimuth of the sun
    azimuth = atan2(
        -cos(decl) * cos(rlat) * sin(hour_ang),
        sin(decl) - sin(rlat) * sin(elevation),
    )
    return (round(azimuth, 2), round(elevation, 2))
