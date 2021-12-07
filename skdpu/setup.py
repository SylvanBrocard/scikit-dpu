import sys
import os

from sklearn._build_utils import cythonize_extensions


def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy

    libraries = []
    if os.name == "posix":
        libraries.append("m")

    config = Configuration("skdpu", parent_package, top_path)

    # submodules with build utilities

    # submodules which do not have their own setup.py
    # we must manually add sub-submodules & tests

    # submodules which have their own setup.py
    config.add_subpackage("tree_dpu")

    # Skip cythonization as we do not want to include the generated
    # C/C++ files in the release tarballs as they are not necessarily
    # forward compatible with future versions of Python for instance.
    if "sdist" not in sys.argv:
        cythonize_extensions(top_path, config)

    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    setup(**configuration(top_path="").todict())
