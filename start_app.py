# -*- coding: utf-8 -*-
"""Helper entry point for running the Gaia 3D simulator.

This file can be set as the startup item in Visual Studio or VS Code. It simply
imports :func:`main` from :mod:`gaia_3d_simulator` and executes it with
``show=True`` so that the generated plot window is displayed automatically.
"""

from gaia_3d_simulator import main

if __name__ == "__main__":
    main(show=True)
