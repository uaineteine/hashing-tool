from setuptools import setup, find_packages

setup(
    name="hash_method",
    version="2.0.0",
    description="A hashing tool module with core and key methods.",
    author="",
    packages=["hash_method"],
    install_requires=[
        "adaptiveio>=1.0.0",
        "pyspark",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)