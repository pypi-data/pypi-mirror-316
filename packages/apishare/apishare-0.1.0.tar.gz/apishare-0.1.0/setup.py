from setuptools import setup, find_packages

setup(
    name="apishare",
    version="0.1.0",
    author="chengangqiang",
    author_email="chengq@niututu.com",
    description="A Python package for API sharing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apishare",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
