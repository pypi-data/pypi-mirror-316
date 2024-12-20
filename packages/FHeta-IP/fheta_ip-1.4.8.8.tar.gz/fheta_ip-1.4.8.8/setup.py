from setuptools import setup, find_packages

setup(
    name="FHeta_IP",
    version="1.4.8.8",
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