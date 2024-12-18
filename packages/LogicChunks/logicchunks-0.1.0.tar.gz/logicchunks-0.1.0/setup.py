from setuptools import setup, find_packages

setup(
    name="LogicChunks",  # The name of your package
    version="0.1.0",     # Initial version
    description="A Python package to divide lists into groups based on conditions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Manikanth Madishatti",
    author_email="manikanthmadishatti4@gmail.com",
    url="https://github.com/yourusername/LogicChunks",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='tests',  # Path to your test suite (the tests/ directory)
    python_requires=">=3.6",
    keywords='python, data structures, lists',  # Keywords for discovery
)

