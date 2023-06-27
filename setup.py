from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in evclinic/__init__.py
from evclinic import __version__ as version

setup(
	name="evclinic",
	version=version,
	description="API for mobile app",
	author="Grabbits",
	author_email="kishan@grabbits.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
