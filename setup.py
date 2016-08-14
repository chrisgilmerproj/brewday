from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.2'

setup(
    name='brewday',
    version=VERSION,
    author='Chris Gilmer',
    author_email='chris.gilmer@gmail.com',
    maintainer='Chris Gilmer',
    maintainer_email='chris.gilmer@gmail.com',
    description='Brew Day Tools',
    url='https://github.com/chrisgilmerproj/brewday',
    download_url='https://github.com/chrisgilmerproj/brewday/tarball/{}'.format(VERSION),  # nopep8
    packages=find_packages(exclude=["*.tests",
                                    "*.tests.*",
                                    "tests.*",
                                    "tests"]),
    scripts=['bin/abv',
             'bin/sugar',
             'bin/temp',
             'bin/yeast'],
    include_package_data=True,
    zip_safe=True,
    tests_require=[
        'nose==1.3.1',
        'pluggy==0.3.1',
        'py==1.4.31',
        'tox==2.3.1',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ),
)
