from setuptools import setup, find_packages

setup(
    name="gimpey_com_sol_gateway",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        "grpcio>=1.50.0",
        "protobuf>=4.0.0",
    ],
    description="Python package for the `gimpey.com` `sol-gateway` service.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gimpey-com/sol-gateway",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
