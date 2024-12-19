from setuptools import setup, find_packages

setup(
    name="subbrute",
    version="1.0.0",
    description="A Python library for brute-forcing subdomains using a wordlist.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url="https://github.com/ByteBreach/subbrute",  
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "subbrute": ["wordlists/default_subdomains.txt"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.0.0",
    ],
    python_requires=">=3.6",
)
