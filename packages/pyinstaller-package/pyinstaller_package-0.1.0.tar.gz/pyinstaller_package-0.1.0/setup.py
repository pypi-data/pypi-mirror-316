from setuptools import setup, find_packages

setup(
    name='pyinstaller_package',  # Name of your package
    version='0.1.0',  # Package version
    packages=find_packages(),  # Automatically find all packages
    install_requires=[  # List of dependencies
        'pyinstaller',
    ],
    entry_points={  # Define a command-line script
        'console_scripts': [
            'generate-executables = pyinstaller_package.executable_generator:generate_executables',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
