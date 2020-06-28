""" Setup file for the COVID-19 Climate Predictor. """
import os
from setuptools import setup

README_PATH = 'README.md'
LONG_DESC = ''

if os.path.exists(README_PATH):
    with open(README_PATH) as readme:
        LONG_DESC = readme.read()

INSTALL_REQUIRES = ['ipykernel', 'jupyter', 'numpy', 'pandas', 'seaborn']
PACKAGE_NAME = 'group10'
PACKAGE_DIR = ''

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    author='group 10',
    author_email='',
    maintainer='Florian Auinger, Florian Butsch, Florian Hoelzl, Christoph Miller,'
    'Johannes Gahr, Johannes Gensheimer, Johannes Kiechle, Constantin Nowak',
    maintainer_email='',
    description="Predictor for measuring the impact of COVID-19 on climate goals.",
    long_description=LONG_DESC,
    license='',
    keywords=['covid-19', 'climate change', 'emissions'],
    url='https://www.ei.tum.de/ldv',
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: PACKAGE_DIR},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['{0} = {0}.{0}:main'.format(PACKAGE_NAME)],
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False
)
