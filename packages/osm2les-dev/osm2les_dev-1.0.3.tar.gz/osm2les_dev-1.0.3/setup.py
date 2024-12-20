
from setuptools import setup, find_packages

setup(
    name='osm2les_dev',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'shapely',
        'osmnx<=1.9.4',
        'rioxarray',
        'rasterio',
        'geopy',
        'geopandas'
    ],
    author='Ranbir Grover',
    author_email='ranbirgrover21@gmail.com',
    description='A package for processing and analyzing LES data with OSM.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://example.com/osm2les_dev',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
