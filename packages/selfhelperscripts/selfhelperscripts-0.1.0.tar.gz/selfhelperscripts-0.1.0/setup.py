from setuptools import setup, find_packages

setup(
    name="selfhelperscripts",
    version="0.1.0",
    author="Mikhail Shche",
    description="Get your life well",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mshegole/selfhelpscripts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.25.1",
        "paramiko>=3.4.0",
    ],
)
