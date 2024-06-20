from setuptools import setup, find_packages

setup(
    name="rbs_pii_anonymizer",
    version="1.0.0",
    description="A python package for text pseudonymization using presidio",
    author="Zein Ramadan",
    author_email="zein.ramadan@bigspark.dev",
    packages=find_packages(include=["anonymizer", "anonymizer.*", "tests", "tests.*"]),
    install_requires=[
        "presidio-analyzer",
        "presidio-anonymizer",
        "spacy"
    ]
)

# python setup.py sdist bdist_wheel
# pip uninstall rbs_pii_anonymizer
# pip install .
