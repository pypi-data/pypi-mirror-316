from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()  # Gets the long description from the README file

setup(
    name='numpyneural',
    version='0.2',
    packages=find_packages(),  # Automatically finds all packages in your project

    author='nndl',
    author_email='nndl@xyz.com',
    description='This is the short description',

    long_description=long_description,  # Long description from README
    long_description_content_type='text/markdown',  # Format of the README
    license='MIT',  # License for your project

    url='https://github.com/your_username/numpyneural',  # Add your project's URL or GitHub link
    classifiers=[  # Classifiers to help others find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    install_requires=[  # List your project dependencies here if needed
        # 'numpy',
        # 'pytorch',
    ],
)
