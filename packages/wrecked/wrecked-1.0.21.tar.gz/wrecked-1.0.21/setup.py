import setuptools
import platform
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
name="wrecked",
version="1.0.21",
author="Quintin Smith",
description="Bindings for the wrecked terminal graphics library",
author_email="smith.quintin@protonmail.com",
long_description_content_type="text/markdown",
url="https://burnsomni.net/git/wrecked",
python_requires=">=3.6",
    install_requires=['cffi'],
    long_description=long_description,
    packages=setuptools.find_packages(),
    package_data={'wrecked': ["libwrecked_manylinux2014_x86_64.so", "libwrecked_manylinux2014_armv7l.so" ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Rust",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
    ]
)
