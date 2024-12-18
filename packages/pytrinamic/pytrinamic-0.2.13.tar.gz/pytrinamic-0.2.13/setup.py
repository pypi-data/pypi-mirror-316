
import setuptools
from pytrinamic.version import __version__

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytrinamic",
    version=__version__,
    author="Trinamic Software Team",
    author_email="tmc_info@trinamic.com",
    description="TRINAMIC's Python Technology Access Package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trinamic/PyTrinamic",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "python-can>=3",
        "canopen",
        "pyserial>=3",
        "IntelHex>=2.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "tmclfwupload = pytrinamic.cli.tmclfwupload:main",
        ]
    }
)
