from setuptools import setup, find_packages


def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        return [
            line.strip() for line in file
            if line.strip() and not line.startswith('#')
        ]


setup(
    name="mxdownloader",
    version="0.1",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        "console_scripts": [
            "mdx = mxdownloader:main",
        ],
    },
)
