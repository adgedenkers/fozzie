from setuptools import setup, find_packages

setup(
    name="fozzie",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "openai",  # Add dependencies as needed
        "requests",
        "pandas",
        "numpy",
        "matplotlib",
        "reportlab",
        "seaborn"
    ],
    author="Adge Denkers",
    description="A utility for data and text analysis and cleaning",
)

