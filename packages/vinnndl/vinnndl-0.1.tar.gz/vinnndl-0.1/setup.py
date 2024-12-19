from setuptools import setup, find_packages

setup(
    name="vinnndl",  # Replace with your package name
    version="0.1",
    packages=find_packages(),
    license="MIT",
    include_package_data=True,  # Ensures data files are included
    description="A package that includes text files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
