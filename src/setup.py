from setuptools import setup
from setuptools import find_packages

long_description = """
# xsens
"""

required = [
    "bleak",
    "numpy"
]

setup(
    name="xsens",
    version="0.0.1",
    author="Jacob Hart",
    url="https://github.com/jdchart/xsens-dot-osc",
    license="GLPv3+",
    author_email="jacob.dchart@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="",
    install_requires=required,
    packages=find_packages()
)