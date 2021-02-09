#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="qiskit-now",
    version="0.1.0",
    author="Salvador de la Puente Gonzalez",
    author_email="salva@unoyunodiez.com",
    description="Qiskit development environment without the configuration pain",
    url="https://github.com/qiskit-community/qiskit-now",
    install_requires=['docker'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'qiskit-now=qiskit_now:main',
        ],
    }
)
