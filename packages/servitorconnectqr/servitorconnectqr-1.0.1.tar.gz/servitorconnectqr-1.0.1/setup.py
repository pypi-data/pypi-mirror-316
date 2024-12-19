from setuptools import setup, find_packages

setup(
    name="servitorconnectqr",
    version="1.0.1",
    author="AnthroHeart (Thomas Sweet)",
    author_email="healing@intentionrepeater.com",
    description="A tool to use Universe Sourcecode with an intention to generate a QR Code.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tsweet77/servitorconnectqr",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "servitorconnectqr=servitorconnectqr.cli:main",
        ],
    },
)
