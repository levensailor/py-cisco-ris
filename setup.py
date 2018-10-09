import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-cisco-ris",
    version="0.0.1",
    author="Jeff Levensailor",
    author_email="jeff@levensailor.com",
    description="Gathers registration status of Cisco IP Phones from CUCM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levensailor/py-cisco-ris",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)