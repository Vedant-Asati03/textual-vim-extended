from setuptools import setup, find_packages

setup(
    name="textual-vim-extended",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "textual>=0.1.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Vim mode extension for Textual TUI framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/textual-vim-extended",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
