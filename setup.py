from setuptools import setup, find_packages

setup(
    name="ComedyClubChallenge",
    version="0.1",
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        "transformers>=4.0",
        "textblob>=0.15.3",
        "torch>=1.8.1",
        "pytest>=6.2.2",
        "hypothesis>=6.79.1",
        "sentence-transformers>=2.2.2",
        "pandas<=2.0.2"
    ],
    author="Konfuzio",
    description="A challenge for Python developers to create AI agents that tell and rate jokes.",
    license="MIT",
)
