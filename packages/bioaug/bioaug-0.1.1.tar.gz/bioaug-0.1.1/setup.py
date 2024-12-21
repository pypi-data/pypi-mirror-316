from setuptools import setup, find_packages

setup(
    name="bioaug",
    version="0.1.1",                     
    author="Peiji Chen",                  
    author_email="peijichen0324@gmail.com",  
    description="A toolbox for biosignal augmentation written in Python",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/peijii/BioAug",  
    packages=find_packages(),            
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",             
    install_requires=[                   
        "numpy", "pandas", "matplotlib", "scipy"],
)
