import os
from pathlib import Path
from setuptools import find_packages, setup
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = os.getenv("VERSION", "1.1.2")

setup(
    name="SON_ZAD2-tests",
    version=version,
    description="Attendance project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SheoTM/SON_ZAD2-tests",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.12",
)