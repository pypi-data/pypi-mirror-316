import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()
NEWS = open(os.path.join(here, "NEWS.rst")).read()


version = "0.7"
install_requires = ["argparse"]

tests_require = [
    "pytest",
]

setup(
    name="lpjsmin",
    version=version,
    description="JS Min script that provides cmd line and python processors",
    long_description=README + "\n\n" + NEWS,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="javascript minification compress",
    author="Rick Harding",
    author_email="rharding@canonical.com",
    url="https://launchpad.net/lpjsmin",
    license="BSD",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    entry_points={"console_scripts": ["lpjsmin=lpjsmin:main"]},
)
