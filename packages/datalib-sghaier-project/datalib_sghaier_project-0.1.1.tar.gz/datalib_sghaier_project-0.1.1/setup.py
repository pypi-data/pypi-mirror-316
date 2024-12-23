from setuptools import setup, find_packages

setup(
    name="datalib_sghaier_project",
    version="0.1.1",
    author="Mazen Sghaier",
    author_email="sghaiermazen7@gmail.com",
    description="A Python library for data manipulation and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MazenSghaier/datalib",  # Update with your repository
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=0.24.0",
    ],
)