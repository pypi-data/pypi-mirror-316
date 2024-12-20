from setuptools import setup, find_packages

setup(
    name="working_ujson",
    version="0.0.1",
    packages=find_packages(),
    description="Working with file package",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    python_requires=">=3.11",
    requires=["ujson"],
)
