from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

setup(
    name="DataChanger",  # Name of the package
    version="0.1.0",  # Version of the package
    description="A class for dot notation access to dictionaries",  # Short description
    author="Adarsh Dhiman",  # Author name
    author_email="adarshdhiman007@gmail.com",  # Author email
    packages=find_packages(),  # Automatically discover and include all packages
    package_data={  # Include non-Python files in the package
        'DataChanger': ['dictator/dot_dict.pyx'],  # Make sure the path to dot_dict.pyx is correct
    },
    ext_modules=cythonize([  # Compile the Cython extension
        Extension('DataChanger.dictator.dot_dict', sources=['dictator/dot_dict.pyx']),  # Ensure the name matches the folder structure
    ]),
    install_requires=[  # List of dependencies
        'Cython',  # Cython is needed to build the extension
    ],
    python_requires='>=3.6',  # Specify the required Python version
)
