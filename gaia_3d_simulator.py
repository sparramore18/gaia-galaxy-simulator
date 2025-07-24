import io
import json
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import Galactocentric, SkyCoord
import pandas as pd
import requests


GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"


def fetch_gaia_data(limit=1000):
    """Fetch a random sample of Gaia DR3 sources using a synchronous TAP query."""
    query = (
        f"SELECT TOP {limit} ra, dec, parallax, pmra, pmdec, radial_velocity "
        "FROM gaiadr3.gaia_source WHERE parallax > 0 ORDER BY random_index"
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


def plot_3d_stars(gc, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(gc.x, gc.y, gc.z, s=1, alpha=0.5)
    ax.set_xlabel("X [kpc]")
    ax.set_ylabel("Y [kpc]")
    ax.set_zlabel("Z [kpc]")
    ax.set_title("Gaia DR3 Stars in Galactocentric Coordinates")
    plt.savefig("gaia_3d.png")
    if show:
        plt.show()
    plt.close()
    print("Saved plot to gaia_3d.png")


def save_star_data_json(gc, filename="gaia_stars.json"):
    """Save Galactocentric coordinates to a JSON file for use with three.js."""
    data = {
        "x": gc.x.to(u.kpc).value.tolist(),
        "y": gc.y.to(u.kpc).value.tolist(),
        "z": gc.z.to(u.kpc).value.tolist(),
    }
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"Saved star coordinates to {filename}")


def generate_threejs_html(gc, html_file="gaia_3d.html", embed_libs=True):
    """Generate a minimal three.js viewer for the star data.

    Parameters
    ----------
    gc : `~astropy.coordinates.SkyCoord`
        Coordinates in the Galactocentric frame.
    html_file : str, optional
        Output HTML filename.
    embed_libs : bool, optional
        If ``True``, the required ``three.js`` libraries are downloaded and
        embedded directly in the HTML. This allows the viewer to work without
        an internet connection. When ``False`` the libraries are loaded from a
        CDN as before.
    """

    data = {
        "x": gc.x.to(u.kpc).value.tolist(),
        "y": gc.y.to(u.kpc).value.tolist(),
        "z": gc.z.to(u.kpc).value.tolist(),
    }

    max_radius = (gc.x**2 + gc.y**2 + gc.z**2) ** 0.5
    max_radius = max_radius.to(u.kpc).max().value

    json_data = json.dumps(data)

    if embed_libs:
        try:
            three_js = requests.get(
                "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js",
                timeout=30,
            ).text
            orbit_js = requests.get(
                "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js",
                timeout=30,
            ).text
            libs = f"<script>{three_js}</script>\n<script>{orbit_js}</script>"
        except Exception as exc:
            print(f"Warning: failed to download three.js libraries: {exc}")
            libs = (
                "<script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script>\n"
                "<script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js'></script>"
            )
    else:
        libs = (
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script>\n"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js'></script>"
        )

    html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='utf-8'>
    <title>Gaia 3D Stars</title>
    <style>body {{ margin: 0; }}</style>
</head>
<body>
{libs}
<script>
const data = {json_data};

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
const controls = new THREE.OrbitControls(camera, renderer.domElement);

const geometry = new THREE.BufferGeometry();
const vertices = [];
for (let i=0; i<data.x.length; i++) {{
    vertices.push(data.x[i], data.y[i], data.z[i]);
}}
geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
const material = new THREE.PointsMaterial({{ color: 0xffffff, size: 0.05 }});
const points = new THREE.Points(geometry, material);
scene.add(points);
camera.position.set(0, 0, {max_radius:.2f});
camera.lookAt(new THREE.Vector3(0, 0, 0));
function animate() {{
    requestAnimationFrame(animate);
    points.rotation.y += 0.0005;
    controls.update();
    renderer.render(scene, camera);
}}
animate();
</script>
</body>
</html>
"""

    with open(html_file, "w") as f:
        f.write(html)
    print(f"Saved HTML viewer to {html_file}")


def main(show=False, open_browser=False):
    data = fetch_gaia_data()
    gc = convert_to_galactocentric(data)
    save_star_data_json(gc)
    generate_threejs_html(gc)
    if open_browser:
        import webbrowser
        webbrowser.open("gaia_3d.html")
    plot_3d_stars(gc, show=show)


if __name__ == "__main__":
    main(open_browser=True)
