import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactocentric
import requests
import pandas as pd
import io


GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"


def fetch_gaia_data(limit=1000):
    """Fetch a small sample of Gaia DR3 sources using a synchronous TAP query."""
    query = (
        f"SELECT TOP {limit} ra, dec, parallax, pmra, pmdec, radial_velocity "
        "FROM gaiadr3.gaia_source WHERE parallax > 0"
    )
    params = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "csv",
        "QUERY": query,
    }
    response = requests.post(GAIA_TAP_SYNC, data=params, timeout=60)
    response.raise_for_status()
    data = pd.read_csv(io.StringIO(response.text))
    print(f"Fetched {len(data)} stars from Gaia")
    return data


def convert_to_galactocentric(data):
    """Convert RA/DEC/parallax to Galactocentric coordinates."""
    mask = data["parallax"] > 0
    data = data[mask]
    c = SkyCoord(
        ra=data["ra"].values * u.deg,
        dec=data["dec"].values * u.deg,
        distance=(1.0 / data["parallax"].values) * u.kpc,
        pm_ra_cosdec=data["pmra"].values * u.mas / u.yr,
        pm_dec=data["pmdec"].values * u.mas / u.yr,
        radial_velocity=data["radial_velocity"].fillna(0).values * u.km / u.s,
        frame="icrs",
    )
    gc = c.transform_to(Galactocentric())
    return gc


def plot_3d_stars(gc):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(gc.x, gc.y, gc.z, s=1, alpha=0.5)
    ax.set_xlabel('X [kpc]')
    ax.set_ylabel('Y [kpc]')
    ax.set_zlabel('Z [kpc]')
    ax.set_title('Gaia DR3 Stars in Galactocentric Coordinates')
    plt.savefig("gaia_3d.png")
    plt.close()
    print("Saved plot to gaia_3d.png")


def main():
    data = fetch_gaia_data()
    gc = convert_to_galactocentric(data)
    plot_3d_stars(gc)


if __name__ == '__main__':
    main()
