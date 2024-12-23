from setuptools import setup, find_packages


setup(
    name="pycbs",
    version="0.1.0",
    author="Markada",
    author_email="markada.py@gmail.com",
    description="CLI Project Compilation Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/your_username/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.13',
)
