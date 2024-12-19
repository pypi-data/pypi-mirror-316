# setup.py
from setuptools import setup, find_packages

setup(
    name="agentCores",
    version="0.2.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        'agentCores': ["data/*"],
    },
    install_requires=[
        "pymongo",
        "duckduckgo_search"
    ],
    include_package_data=True,
    python_requires=">=3.8",
    author="Leo Borcherding",
    description="A flexible framework for creating and managing AI agent configurations with sqlite3 & json",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Leoleojames1/agentCores",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)