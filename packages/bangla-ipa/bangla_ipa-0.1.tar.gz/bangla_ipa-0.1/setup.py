import os
# import chardet
from setuptools import setup, find_packages


# def detect_file_encoding(filename):
#     with open(filename, "rb") as f:
#         result = chardet.detect(f.read())
#     return result
#
#
# encoding_info = detect_file_encoding("requirements.txt")
# print(encoding_info)
#
#
# def convert_to_utf8(filename):
#     with open(filename, "rb") as f:
#         content = f.read()
#
#     encoding = chardet.detect(content)["encoding"]
#     if encoding != "utf-8":
#         with open(filename, "w", encoding="utf-8") as f:
#             f.write(content.decode(encoding))
#
#
# convert_to_utf8("requirements.txt")


def parse_requirements_safe(filename):
    with open(filename, "r", encoding="utf-8") as file:
        requirements = []
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore blank lines and comments
                requirements.append(line)
        return requirements


requirements = parse_requirements_safe("requirements.txt")


# parse requirements
def parse_requirements(filename):
    """
    Parse a requirements file, ignoring comments and blank lines.
    Args:
        filename (str): The path to the requirements file.
    Returns:
        list: A list of requirement strings.
    """
    requirements = []
    with open(filename, "rb") as file:
        for line in file:
            line = line.decode("utf-8-sig").strip()
            if line and not line.startswith("#"):  # Ignore blank lines and comments
                requirements.append(line)
    return requirements


# Get the absolute path of the current directory
here = os.path.abspath(os.path.dirname(__file__))

# Read and parse requirements.txt
requirements = parse_requirements(os.path.join(here, "requirements.txt"))

# Read README.md for the long description
with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# Setting up the package
setup(
    name="bangla-ipa",
    version="0.1",
    author="Biplab Kumar Sarkar, Afrar Jahin, Asif Shusmit",
    author_email="bip.sec22@gmail.com",
    description="A Python module for generating Bangla IPA transliterations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bipsec/IPA-PyPI",
    license="MIT",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": ["model/ipa_model.pth", "data/ipa_vocab_data/*"],
    },
    keywords=[
        "python", "IPA", "Bangla IPA", "International Phonetic Alphabet",
        "Bangla linguistics", "transliteration"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
