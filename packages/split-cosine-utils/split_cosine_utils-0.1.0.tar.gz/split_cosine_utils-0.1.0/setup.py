from setuptools import setup, find_packages

setup(
    name="split_cosine_utils",
    version="0.1.0",
    description="A utility package for data splitting and cosine similarity computations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/split_cosine_utils",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)