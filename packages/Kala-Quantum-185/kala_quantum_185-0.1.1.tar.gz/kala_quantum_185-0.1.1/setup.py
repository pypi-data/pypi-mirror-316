from setuptools import setup, find_packages

setup(
    name="Kala_Quantum_185",
    version="0.1.1",
    description="A hybrid classical-quantum framework for code language modeling.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    url="https://github.com/kalasaikamesh944/kala_quantum",  # Replace with your GitHub repo
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=1.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
