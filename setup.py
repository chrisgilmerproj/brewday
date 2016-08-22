from setuptools import find_packages
from setuptools import setup


VERSION = '0.0.4'

setup(
    name='brewday',
    version=VERSION,
    author='Chris Gilmer',
    author_email='chris.gilmer@gmail.com',
    maintainer='Chris Gilmer',
    maintainer_email='chris.gilmer@gmail.com',
    license="MIT",
    description='Brew Day Tools',
    url='https://github.com/chrisgilmerproj/brewday',
    download_url='https://github.com/chrisgilmerproj/brewday/tarball/{}'.format(VERSION),  # nopep8
    packages=find_packages(exclude=["*.tests",
                                    "*.tests.*",
                                    "tests.*",
                                    "tests"]),
    entry_points={
        'console_scripts': [
            'abv = brew.cli.abv:main',
            'sugar = brew.cli.sugar:main',
            'temp = brew.cli.temp:main',
            'yeast = brew.cli.yeast:main',
        ],
    },
    include_package_data=True,
    zip_safe=True,
    tests_require=[
        'nose==1.3.1',
        'pluggy==0.3.1',
        'py==1.4.31',
        'tox==2.3.1',
    ],
    keywords='brew brewing beer grain hops yeast alcohol',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
