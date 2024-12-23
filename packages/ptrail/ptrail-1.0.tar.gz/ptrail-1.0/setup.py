from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

REQUIRED_PKGS = ['numpy >= 1.20',
                 'hampel >= 0.0.5',
                 'pandas >= 1.2.5',
                 'scipy >= 1.6.2',
                 'folium >= 0.12',
                 'osmnx >= 1.1.1',
                 'geopandas >= 0.8.1',
                 'shapely',
                 'IPython >= 7.27.0',
                 'ipywidgets >= 7.6.5',
                 'plotly >= 5.3.1',
                 'matplotlib >= 3.3.4',
                 'seaborn >= 0.11.2',
                 'PyQt5',
                 'scikit-learn >= 0.24.2',
                 ]

setup(
    name='ptrail',
    packages=find_packages(),
    version='1.0',
    license='new BSD',
    python_requires='>=3.6',
    description='PTRAIL: A Mobility-data Preprocessing Library using parallel computation.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    maintainer='PTRAIL Developers',
    maintainer_email='yjharanwala@mun.ca',
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 ],
    install_requires=REQUIRED_PKGS,
    url='https://github.com/YakshHaranwala/PTRAIL.git',
    include_package_data=True,
)
