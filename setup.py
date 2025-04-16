from setuptools import setup, find_packages

setup(
    name="fozzie",
<<<<<<< HEAD
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        # add any other dependencies you use here
    ],
    entry_points={
        'console_scripts': [
            'foz=fozzie.cli:cli',
        ],
    },
)
=======
    version="0.2.1",
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

>>>>>>> 693e44138d24d3e682a1a8297cb8d141f08948a9
