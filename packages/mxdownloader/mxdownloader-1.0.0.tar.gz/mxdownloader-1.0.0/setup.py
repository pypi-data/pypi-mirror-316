from setuptools import setup, find_packages


def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        return [
            line.strip() for line in file
            if line.strip() and not line.startswith('#')
        ]


setup(
    name="mxdownloader",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mdx = mxdownloader:main",
        ],
    },
    description="Download Manga using the MangaDex API",
    license="MIT",
    long_description=
    "A Python CLI tool to download manga using the MangaDex API. Visit the GitHub page for more info.",
    url="https://github.com/Hiro427/mxdownloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Jacob Rambarran",
    install_requires=parse_requirements('requirements.txt'),
)
