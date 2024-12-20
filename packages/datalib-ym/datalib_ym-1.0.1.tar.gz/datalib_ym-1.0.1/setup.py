from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datalib_ym",
    version="1.0.1",
    author="Yessine Miled",
    author_email="miled.yassine7@gmail.com",
    description="A comprehensive library for data manipulation, analysis, and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miledyessine/datalib_ym",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.1.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
        "scikit-learn>=0.23.0",
        "scipy>=1.5.0",
    ],
)

