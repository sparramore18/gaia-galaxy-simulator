# Gaia Galaxy Simulator

This project provides a simple test-particle orbit integration using the `galpy` library in a smooth Milky Way potential. It also includes a small 3‑D visualisation of real Gaia DR3 stars. The code can serve as a starting point for developing a more realistic galaxy simulator using Gaia data.

## Requirements

- Python 3.9 or later
- galpy, numpy, astropy, matplotlib, pandas, astroquery

Install the dependencies with pip:

pip install galpy numpy astropy matplotlib pandas astroquery

Or with conda:

conda install -c conda-forge galpy numpy astropy matplotlib pandas astroquery

## Running

The file `orbit_simulation.py` contains an example of integrating a single test particle orbit. Run it from the command line with:

python orbit_simulation.py

It will integrate the orbit for 10 Gyr and plot the orbit in the x–y plane.

The script `gaia_3d_simulator.py` downloads a small sample of stars from Gaia DR3 and shows them in 3‑D Galactocentric coordinates. Run it as:

```bash
python gaia_3d_simulator.py
```

The query may take a few seconds as it retrieves data from the online Gaia archive. When finished, a PNG image called `gaia_3d.png` is created in the current directory.

To automatically display the generated image, run the helper script:

```bash
python start_app.py
```

## Using Visual Studio or VS Code

1. Clone this repository and open it in Visual Studio or VS Code.
2. Select a Python interpreter (version 3.9+).
3. (Optional) Create a virtual environment with `python -m venv .venv` and activate it.
4. Install the dependencies as listed above.
5. Run `orbit_simulation.py` via the Run/Debug panel or by pressing F5.

## Next Steps

Possible future improvements include adding more orbits, using the `gala` library for more complex potentials, and incorporating Gaia DR3 data. Use the provided GitHub project board (Gaia Galaxy Simulator Project) to track tasks and progress.

---

*This README was updated to provide instructions for running the code and using Visual Studio.*
