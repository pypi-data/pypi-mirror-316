from setuptools import setup, find_packages

setup(
    name="grease-embeddings",
    version="0.1.0",
    description="Generalizable and Efficient Approximate Spectral Embeddings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nir Ben-Ari",
    author_email="nirnirba@gmail.com",
    url="https://github.com/TheNirnir/GrEASE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
