from setuptools import setup, find_packages
import pathlib
setup(
    name='plasan',
    version='0.1',
    desciption='Breif description of the package',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'biopython',
        'pycirclize',
        'gdown',
        
        # add others here as well - prodigal, blast, etc.
    ],
    entry_points={
        "console_scripts": [
            "PlasAnn = plasan.main:PlasAnn"
        ],
    },
)




