from setuptools import setup, find_packages
import pathlib

VERSION = '0.0.9'
DESCRIPTION = 'Simple python package'


# Read the contents of the README.md file
current_directory = pathlib.Path(__file__).parent.resolve()
LONG_DESCRIPTION = (current_directory / "README.md").read_text(encoding="utf-8")

# Setting up
setup(
        # the name must match the folder name 'verysimplemodule'
        name="re_matrix",
        version=VERSION,
        author="Charlie",
        author_email="<charlie@thatcharlie.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",  # Indicate Markdown format
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