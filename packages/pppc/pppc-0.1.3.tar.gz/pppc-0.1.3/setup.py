from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pppc",
    version="0.1.3",
    author="retrotee",
    description="Create Minecraft Paper plugins using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/retrotee/pppc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",         # For YAML file handling
        "typing-extensions>=4.0.0",  # For enhanced type hints
        "dataclasses>=0.6",    # For Python 3.6 compatibility
        "jinja2>=3.0.0",       # For template rendering
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'mypy>=0.950',
            'flake8>=4.0.0',
            'tox>=3.24.0'
        ]
    }
)