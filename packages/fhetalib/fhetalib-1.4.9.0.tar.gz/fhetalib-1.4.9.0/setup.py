from setuptools import setup, find_packages

setup(
    name="fhetalib",
    version="1.4.9.0",
    description="",
    author="FHeta",
    packages=find_packages(),
    install_requires=[
        "telethon",
        "requests",
        "flask",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)