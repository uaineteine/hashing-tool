from setuptools import setup, find_packages

setup(
    name="hash_method",
    version="2.0.0",
    description="A hashing tool module with core and key methods.",
    author="",
    packages=["adaptiveio", "pyspark"],
    install_requires=[
        # Add any dependencies from requirements.txt here
    ],
    python_requires=">=3.10",
    include_package_data=True,
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)