from setuptools import setup, find_packages

setup(
    name="jaya-optimizer",
    version="0.1.2",
    author="Ravikumar Shah",
    author_email="ravikumar.shah.2804@gmail.com",
    description="A Python library implementing the Jaya Optimization Algorithm.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ravikumar-Shah-2804/jaya-optimizer.git",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
