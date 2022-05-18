import numpy as np

def CalcEnergy(L, l, alpha, beta, eta, lat, weather):
    # Inputs :
    # L : length of solar panels
    # l : width
    # alpha : inclination angle in °, 0 flat on ground 90° standing
    # beta : orientation towards south, 0° full South, 90° East
    # eta : efficiency of panel [0;1]
    # lat : latitude of building
    # weather : solar radiation energy per hour in a year [Wh/m^2]

    alpha = alpha * np.pi / 180
    beta = beta * np.pi / 180

    phi = lat / 180 * np.pi

    day = np.arange(0, 365)
    deltas = 23.45 * np.sin(2 * np.pi * ((day - 81) / 365)) / 180 * np.pi
    hour = np.arange(0, 24)
    h = np.zeros(0)
    a = h
    for i in day:
        hd = np.arcsin(
            np.sin(phi) * np.sin(deltas[i]) + np.cos(phi) * np.cos(deltas[i]) * np.cos(15 * (hour - 12) / 180 * np.pi))
        h = np.append(h, hd)
        had = np.arcsin(
            np.sin(phi) * np.sin(-deltas[i]) + np.cos(phi) * np.cos(deltas[i]) * np.cos(15 * (hour - 12) / 180 * np.pi))
        ad = np.arcsin(np.cos(deltas[i]) / np.cos(had) * np.sin(15 * (hour - 12) / 180 * np.pi))
        a = np.append(a, ad)

    # Set the night values to 0
    h = np.clip(h, 0, None)

    for i in range(len(a)):
        if i == len(a) - 1:
            #print("modifing last value")
            a[i] = np.pi / 2
        elif a[i] > a[i + 1]:
            a[i] = np.pi / 2

    # plt.plot(h)
    # plt.legend(['Hauteur'])
    # plt.xlabel('Temps [h]')
    # plt.ylabel('Angle [rad]')
    # plt.title('Hauteur')
    # plt.show()

    # plt.plot(a)
    # plt.legend(['azimut'])
    # plt.xlabel('Temps [h]')
    # plt.ylabel('Angle [rad]')
    # plt.title('Azimut')
    # plt.show()

    # Solar panel shadow calculation
    hp = L * np.sin(alpha) + L * np.cos(alpha) * np.tan(h)
    lp = l * np.sin(beta + np.pi / 2 - a)
    s = np.multiply(hp, lp)

    # Energy produced
    e = np.multiply(s, weather) * eta

    return e
