from setuptools import setup, find_packages

setup(
    name="datalib-isimm",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.9",
            "sphinx>=4.0",
        ],
    },
    python_requires=">=3.8",
    author="Yassine Saidane",
    author_email="yassinesaidane003@gmail.com",
    description="Une bibliothèque Python pour la manipulation et l'analyse de données",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/datalib",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 