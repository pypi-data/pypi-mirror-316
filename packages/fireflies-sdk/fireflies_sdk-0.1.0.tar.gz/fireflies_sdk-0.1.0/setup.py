from setuptools import setup, find_packages

setup(
    name="fireflies-sdk",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    author="David Schwartz",
    author_email="david.schwartz@devfactory.com",
    description="SDK for interacting with Fireflies.ai API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trilogy-group/pocs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
