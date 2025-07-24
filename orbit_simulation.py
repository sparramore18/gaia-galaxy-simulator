import numpy as np
import matplotlib.pyplot as plt
from galpy.orbit import Orbit
from galpy.potential import MilkyWayPotential
from galpy.util import bovy_conversion
from astropy import units as u

# Example: integrate a test particle orbit in a smooth Milky Way potential
def simulate_orbit():
    # Define initial conditions: radius 8 kpc, tangential velocity 220 km/s
    o = Orbit([8, 0.0, 0.0, 0.0, 220/bovy_conversion.vcirc(8, MilkyWayPotential), 0.0])
    ts = np.linspace(0, 10, 1000) * u.Gyr  # 0 to 10 Gyr
    o.integrate(ts, MilkyWayPotential)
    # Convert to galactocentric coordinates (x-y plane)
    x = o.x(ts)
    y = o.y(ts)
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('x [kpc]')
    plt.ylabel('y [kpc]')
    plt.title('Test Particle Orbit in Milky Way Potential')
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    simulate_orbit()
