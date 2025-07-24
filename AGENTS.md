# AGENTS Instructions for Gaia Galaxy Simulator

This file provides guidance for contributors interacting with this repository.
The instructions apply to all directories in this repository.

## Repository Overview

The codebase contains small Python scripts that demonstrate basic orbit
integration with **galpy** and retrieval/visualisation of Gaia DR3 star data.
The main files are:

- `orbit_simulation.py` – integrates a simple test particle orbit.
- `gaia_3d_simulator.py` – downloads a random sample of Gaia stars, converts
  them to Galactocentric coordinates and generates both a static plot and an
  interactive three.js viewer.
- `start_app.py` – convenience entry point used by IDEs, running the simulator
  with some defaults.
- `requirements.txt` – dependencies required to execute the scripts.

## Contribution Guidelines

- **Python version**: code should remain compatible with Python 3.9 or later.
- **Style**: follow [PEP 8](https://peps.python.org/pep-0008/) with
  4‑space indentation and lines no longer than 88 characters when practical.
  Include module, function and class docstrings where appropriate.
- **Commit messages**: use short imperative statements summarising the change.
- **Pull requests**: describe what was changed and how to run any affected
  scripts.

## Programmatic Checks

Before committing changes that modify Python files, run the following command
from the repository root to ensure all scripts compile:

```bash
python -m py_compile gaia_3d_simulator.py orbit_simulation.py start_app.py
```

These checks are lightweight and confirm that the code is at least syntactically
correct. If dependencies are missing you may need to install them with:
`pip install -r requirements.txt`.

If adding new scripts, include them in the compilation command when possible.

## Documentation

- Keep this `AGENTS.md` up to date when new conventions or checks are added.
- Document new features or instructions in the `README.md`.

---

*End of AGENTS instructions.*
