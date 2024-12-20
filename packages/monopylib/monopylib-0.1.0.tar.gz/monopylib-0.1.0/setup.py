from setuptools import setup, find_packages

setup(
    name="monopylib",
    version="0.1.0",
    author="Yakov Perets",
    author_email="yakov.perets@gmail.com",
    description="Tool for managing Python monorepos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Specify Markdown format
    url="https://gitlab.com/yakov.perets/python-monorepo-simulation",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "monopylib=monopylib.init.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
