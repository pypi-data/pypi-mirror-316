from setuptools import setup, find_packages

setup(
    name="sdw_tools",                   # Your library name
    version="0.1.0",                     # Library version
    author="D",
    author_email="divij.d@students.iiit.ac.in",
    description="This library can be used for fetching data from github repositories and calculating the Software Development Waste associated with the repository.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DivijD012/sdw_tools",  # Project URL
    packages=find_packages(),            # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",             # Minimum Python version
    install_requires=[
        "requests",                      # Add dependencies here
        "numpy",
        "scikit-learn",
        "matplotlib",
    ],
)
