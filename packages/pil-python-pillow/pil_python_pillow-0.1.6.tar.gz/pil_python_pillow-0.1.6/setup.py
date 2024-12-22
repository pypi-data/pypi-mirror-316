from setuptools import setup, find_packages

setup(
    name="pil_python_pillow",
    version="0.1.6",
    author="Tawfiq",
    author_email="twfyqbhyry4@gmail.com",
    description="A lightweight SQL compiler using PLY",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tawfiqbhyry/compiler_test",
    packages=find_packages(),
    install_requires=[
        "numpy",  # Dependency for lex and yacc
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
