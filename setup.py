from setuptools import setup, find_packages

setup(
    name="github-repo-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygount>=1.5.0",
    ],
    entry_points={
        "console_scripts": [
            "repo-analyzer=src.analyzer:main",
        ],
    },
    author="Femirins",
    description="Autonomous GitHub Repository Analyzer",
    license="MIT",
)