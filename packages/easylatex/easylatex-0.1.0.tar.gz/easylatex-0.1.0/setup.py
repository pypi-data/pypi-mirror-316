from setuptools import setup, find_packages

setup(
    name="easylatex",  # Unique name on PyPI
    version="0.1.0",  # Update this for each new version
    author="Sagar Paul",
    author_email="sagarpaul.dev@gmail.com",
    description="Simplify writing LaTeX documents with Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
