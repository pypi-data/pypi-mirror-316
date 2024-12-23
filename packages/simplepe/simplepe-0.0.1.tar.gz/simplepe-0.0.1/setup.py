from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="simplepe",
    packages=find_packages(),
    version="0.0.1",
    author="Dong Linkang",
    author_email="donglinkang2021@163.com",
    description="A simple simplepe for positional encoding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donglinkang2021/simplepe",
    keywords = [
        'artificial intelligence',
        'deep learning',
        'positional embedding'    
    ],
    install_requires=[
        'torch>=2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)