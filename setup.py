import os
import sys

from distutils.util import convert_path
from setuptools import find_packages, setup


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


# Get global version
# see: https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
ver_path = convert_path(
    f"{get_script_path()}/src/stock/version.py"
)
with open(ver_path) as ver_file:
    exec(ver_file.read(), version)

REQUIREMENTS = ["Click", "click-log", "python-dotenv", "requests"]
EXTRAS_REQUIRES = {"app": ["jina[http]", "requests", "streamlit", "torch", "transformers"]}

setup(
    name="stock",
    description="An ML-powered web app for stock image semantic search",
    version=version["__version__"],
    author="Tim Gibson",
    license="Apache 2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7.0, <3.9.0",
    entry_points={"console_scripts": ["stock=stock.cli:main"]},
    install_requires=REQUIREMENTS,
    include_package_date=True,
    test_suite="tests",
    extras_require=EXTRAS_REQUIRES,
    zip_safe=False,
)
