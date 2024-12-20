from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Simple python package for row reducing matrices'
LONG_DESCRIPTION = 'Simple python package for row reducing matrices'

# Setting up
setup(
        # the name must match the folder name 'verysimplemodule'
        name="re_matrix",
        version=VERSION,
        author="Charlie",
        author_email="<charlie@thatcharlie.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],  # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'matrices', 'row reduction', 'linear algebra'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)