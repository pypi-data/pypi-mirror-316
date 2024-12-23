from setuptools import setup, find_packages

setup(
    name="Dcleanser",                # Package name
    version="0.1",                      # Version number
    author="Mukil",                     # Your name
    description="A module to auto clean data frames.",  # Short description
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),           # Automatically find all sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",            # Minimum Python version
)
