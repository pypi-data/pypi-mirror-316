from setuptools import setup, find_packages

setup(
    name="crypto-cli-tool",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "crypto.cli=crypto_cli:main",
        ],
    },
    author="Your Name",
    description="A CLI tool to fetch cryptocurrency prices.",
    url="https://github.com/yourusername/crypto-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
