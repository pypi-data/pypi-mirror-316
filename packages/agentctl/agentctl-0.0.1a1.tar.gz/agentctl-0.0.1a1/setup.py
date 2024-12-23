from setuptools import setup, find_packages

setup(
    name="agentctl",
    version="0.0.1-alpha1",
    author="Andrii Tsok",
    author_email="andrii@tsok.org",
    description="A minimal Python package for agent control",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/agentctl/agentctl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
