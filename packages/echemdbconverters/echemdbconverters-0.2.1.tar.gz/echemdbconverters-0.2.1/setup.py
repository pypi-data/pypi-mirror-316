# *********************************************************************
#  This file is part of echemdb-converters.
#
#        Copyright (C) 2023 Albert Engstfeld
#
#  echemdb-converters is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  echemdb-converters is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with echemdb-converters. If not, see <https://www.gnu.org/licenses/>.
# *********************************************************************
from distutils.core import setup

setup(
    name="echemdbconverters",
    version="0.2.1",
    packages=["echemdbconverters", "echemdbconverters.test"],
    license="GPL 3.0+",
    description="echemdb-converters is a Python library and command line tool to load csv data and convert those into frictionless datapackages.",
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "clevercsv",
        "click>=8,<9",
        "frictionless>=5,<6",
        "pandas",
        "unitpackage>=0.8.4,<0.9.0",
    ],
    entry_points={
        "console_scripts": ["echemdbconverters=echemdbconverters.entrypoint:cli"],
    },
    python_requires=">=3.9",
)
