# setup.py
from setuptools import setup, find_packages

setup(
    name='ppgames',                   # Name of the package
    version='0.1.5',    # Version of the package
    packages=find_packages(),         # Automatically find the packages in the directory
    install_requires=[],              # List any external dependencies (none for this game)
    author='PYTHON PAVAN',            # Your name
    author_email='pavan.sidd2004@gmail.com',  # Your email
    description='A simple game designed by PythonPavan',  # Short description
    long_description=open('README.md').read(),  # Read detailed description from README
    long_description_content_type='text/markdown',  # Set content type to markdown
    url='https://github.com/pythonpavan04/ppgames',  # Link to your GitHub or repository
    classifiers=[                     # Classifiers for PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={                     # Entry point for command-line script (optional)
        'console_scripts': [
            'ppgames = ppgames.game:run',  # Run the game from the command line
        ],
    },
)
