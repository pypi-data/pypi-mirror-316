from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mmetrics',  
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-image',
        'scikit-learn', 
        'pytorch-fid', 
        'torch'
    ],
    author='Angie Carrillo',  
    author_email='a.carrillo@stariongroup.eu',
    description='A library to perform image quality and classification assessment.',
    long_description=long_description,  # Include README content
    long_description_content_type="text/markdown",  # Specify Markdown format
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    

)