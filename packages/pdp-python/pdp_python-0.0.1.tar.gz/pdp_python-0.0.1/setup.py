from setuptools import setup, find_packages

setup(
    name="pdp_python",
    version="0.0.1",
    packages=find_packages(),
    description="Arithmetic operations package",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    python_requires=">=3.11"
)
