from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='whats_going_on',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)