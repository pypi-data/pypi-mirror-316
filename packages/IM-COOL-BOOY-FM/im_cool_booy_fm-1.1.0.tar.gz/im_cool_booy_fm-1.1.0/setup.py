from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="IM-COOL-BOOY-FM",
    version="1.1.0",
    author="IM COOL BOOY",
    author_email="coolbooy@gmail.com",
    description="A tool for streaming radio stations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IM-COOL-HACKER-BOOY/IM-COOL-BOOY-FM.git",
    packages=["IM_COOL_BOOY_FM"],
    install_requires=[
        "requests>=2.25.0",
        "python-vlc>=3.0.1115",
        "colorama>=0.4.4",
    ],
    entry_points={
        'console_scripts': [
           'IM-COOL-BOOY-FM=IM_COOL_BOOY_FM.main:main',
         ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
