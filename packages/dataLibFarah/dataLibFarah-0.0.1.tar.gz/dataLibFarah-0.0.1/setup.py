from setuptools import setup, find_packages

setup(
    name="dataLibFarah",
    version="0.0.1",
    author="Farah Riahi",
    author_email="farah.riahi2@gmail.com",
    description="A library for data manipulation, analysis, and visualization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/riahiFarah/DataLib.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0",
        "numpy>=1.19",
        "matplotlib>=3.0",
        "scikit-learn>=0.24",
        "scipy>=1.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "twine>=4.0.2"
        ]
    },
    entry_points={
        "console_scripts": []
    },
    include_package_data=True,
)
