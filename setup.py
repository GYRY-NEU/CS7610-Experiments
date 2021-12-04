import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Simulation",
    version="0.0.1",
    author="Gokberk Ryan",
    author_email="yargokberk1998@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GYRY-NEU/Simulation",
    project_urls={
        "Bug Tracker": "https://github.com/GYRY-NEU/Simulation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fabric',
        'parse',
        'numpy',
        'pandas',
        'matplotlib'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['simulation=Simulation.main:main']
    }

)