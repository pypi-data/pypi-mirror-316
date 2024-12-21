from setuptools import setup, find_packages

setup(
    name='mmetrics',  
    version='1.0.0',
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
    description='A .',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)