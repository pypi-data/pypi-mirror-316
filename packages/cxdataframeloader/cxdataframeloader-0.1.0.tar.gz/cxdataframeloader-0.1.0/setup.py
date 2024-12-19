from setuptools import setup, find_packages

setup(
    name='cxdataframeloader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "pandas==2.2.2"
        ,"plotly==5.22.0"   
    ]
)
