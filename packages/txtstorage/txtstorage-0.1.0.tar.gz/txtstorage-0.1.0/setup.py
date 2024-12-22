from setuptools import setup, find_packages

setup(
    name="txtstorage",
    version="0.1.0",
    author="Logan Harper",
    author_email="negro@gmail.com",
    description="silly silly sily suilly isilly silly",
    url="https://github.com/yourusername/timetrack",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change if you use a different license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
    install_requires=[
        "requests",
    ],
)