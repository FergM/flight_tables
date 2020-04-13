import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flight_tables",
    version="v1.0",
    author="FergM",
    description="Save (Heathrow) Airport Arrivals and Departures to CSV.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FergM/flight_tables/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4>=0.0.1',
        'pandas>=0.25.3',
        'requests>=2.23.0',
    ]
    python_requires='>=3.6',
)
