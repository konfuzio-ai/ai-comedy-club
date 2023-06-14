from setuptools import setup, find_packages

setup(
    name="ComedyClubChallenge",
    version="0.1",
    packages=find_packages(),

    install_requires=[
        "transformers>=4.0",
        "textblob>=0.15.3",
        "torch>=1.8.1",
        "pytest>=6.2.2"
    ],

    author="Konfuzio",
    description="A challenge for Python developers to create AI agents that tell and rate jokes.",
    license="MIT",
)
