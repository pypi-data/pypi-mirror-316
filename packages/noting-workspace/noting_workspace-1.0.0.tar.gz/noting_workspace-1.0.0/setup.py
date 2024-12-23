from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='noting-workspace',
    version='1.0.0',
    description='A lightweight and efficient notebook application for organizing your ideas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='None',
    author_email='',
    license='',
    zip_safe=False,
    include_package_data=False

)