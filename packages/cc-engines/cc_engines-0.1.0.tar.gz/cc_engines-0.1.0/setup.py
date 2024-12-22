from setuptools import setup, find_packages

setup(
    name="cc_engines",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "chess",
        "numpy",
    ],
)