from setuptools import setup, find_packages

setup(
    name='Estar',  # The name of your package
    version='1.5',  # The version of your package
    packages=find_packages(),  # Automatically finds all the submodules
    install_requires=[  # List any external dependencies
        'numpy',        # Example dependencies
        'matplotlib',
        'scikit-learn',
        'tiffile',
        'Pillow',          # PIL might not be available, use 'Pillow' instead
        'scipy',
        'scikit-image', # Correct package name for 'skimage'
        'rasterio',
        'pyproj',
        'pandas',
        'shapely',
        'geopandas',
    ],
    # Uncomment below if you want to test with pytest
    # tests_require=['pytest'],  # If you're using pytest for testing
    # test_suite='tests',  # Folder containing your tests
)