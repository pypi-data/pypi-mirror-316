from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="genio-telegram",
    version="0.1.1",
    author="Kunal Gaikwad",
    author_email="kunalgaikwad9322@gmail.com",
    description="A Gen Z-inspired Telegram MTProto API framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KunalG932/genio",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "typing-extensions>=4.0.0"
    ],
)
