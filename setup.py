# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from contratacion import __version__


setup(
    name='contratacion',
    version=__version__,
    description='Contrataciondelestado.es web data scraper',
    author='Javier Santacruz',
    author_email='javier.santacruz.lc@gmail.com',
    url='https://github.com/jvrsantacruz/contratacion',
    packages=find_packages(exclude=['spec', 'spec.*']),
    install_requires=[
        'SQLAlchemy',
        'booby',
        'cssselect',
        'docopt',
        'pyquery',
        'python-dateutil',
        'requests',
        'simplekv',
        'Flask',
        'Flask-RESTful'
    ],
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    platforms=['Unix'],
    entry_points={
        'console_scripts': ['contratacion = contratacion.cli:main']
    }
)
