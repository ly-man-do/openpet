# SPDX-License-Identifier: Apache-2.0
from glob import glob

from setuptools import find_packages, setup

package_name = "openpet_bringup"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "hello = openpet_bringup.hello:main",
        ],
    },
)
