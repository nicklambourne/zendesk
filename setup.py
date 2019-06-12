from setuptools import setup, find_packages

requirements = [
    "pytest",
    "zenpy"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zendesk",
    version="0.0.1",
    packages=find_packages(),
    url="https://github.com/nicklambourne/elpis",
    install_requires=requirements,
    install_package_data=True,
    license="BSD",
    author="Nicholas Lambourne",
    author_email="nick@ndl.im",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={

    },
)
