from setuptools import setup, find_packages

# 讀取 README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mathalgo",
    version="1.0.0",
    author="Donseking",
    author_email="0717albert@gmail.com",
    description="A Python module for mathematical algorithms and data structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Donseking/MathAlgo",
    project_urls={
        "Bug Tracker": "https://github.com/Donseking/MathAlgo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'flake8>=3.9.0',
        ],
    }
) 