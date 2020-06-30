import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Frontiersman-ForgedSnow", # Replace with your own username
    version="1.0.0",
    author="Brian Snow",
    author_email="snowb@ufl.edu",
    description="Settlers of Catan style multiplayer Desktop Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ForgedSnow/Frontiersman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)