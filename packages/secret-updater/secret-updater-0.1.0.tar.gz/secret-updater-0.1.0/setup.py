from setuptools import setup, find_packages

setup(
    name="secret-updater",
    version="0.1.0",
    author="Daniel Nebenzahl",
    author_email="dn@scribesecurity.com",
    description="CLI tool to update GitHub repository secrets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/scribe-security/secret-updater",
    packages=["secret_updater"],
    package_dir={"secret_updater": "secret_updater"},
    install_requires=["requests", "pynacl"],
    entry_points={
        "console_scripts": [
            "secret-updater=secret_updater.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
