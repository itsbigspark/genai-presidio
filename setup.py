from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Install required packages
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        # Ensure the spaCy model is downloaded
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])
        install.run(self)

setup(
    name="my_anonymizer",
    version="0.1.0",
    description="A package for text anonymization and deanonymization using Presidio and OpenAI",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "presidio-analyzer",
        "presidio-anonymizer",
        "pydantic",
        "openai",
        "spacy"
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)

# python setup.py sdist bdist_wheel
# pip uninstall rbs_pii_anonymizer
# pip install .
