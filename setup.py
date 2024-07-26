# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="easy-llms",
    description="Easy '1-line' calling of every LLM from OpenAI, MS Azure, AWS Bedrock, GCP Vertex, and Ollama",
    version="0.1.12",
    author="Ventz Petkov",
    url="https://github.com/ventz/easy-llms",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=required,
    include_package_data=True,
    #extras_require={"dev": ["pytest""]},
    # Coming soon!
    #test_suite="tests",
)
