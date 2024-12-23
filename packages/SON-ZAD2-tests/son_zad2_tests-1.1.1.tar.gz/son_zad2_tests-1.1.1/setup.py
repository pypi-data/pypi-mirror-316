import os

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = os.getenv("VERSION", "1.1.1")



setup(
    name="SON_ZAD2-tests",
    version=version,
    description="Attendance project",
    url="https://github.com/SheoTM/SON_ZAD2-tests",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.12",
)