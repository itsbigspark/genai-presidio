from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # Ensure the spaCy model is downloaded
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])
        install.run(self)


setup(
    name="rbs_pii_anonymizer",
    version="1.0.0",
    description="A python package for text pseudonymization using presidio",
    author="Zein Ramadan",
    author_email="zein.ramadan@bigspark.dev",
    packages=find_packages(),
    install_requires=[
        "presidio-analyzer",
        "presidio-anonymizer",
        "spacy"
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)

# python setup.py sdist bdist_wheel
# pip uninstall rbs_pii_anonymizer
# pip install .
