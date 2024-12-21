import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()


setuptools.setup(
    name="caerp_split_pdf",
    version="2024.1.0",
    author="Arezki Feth",
    author_email="tech@majerti.fr",
    description="Splits specific PDF files and stores the result in a custom directory layout",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    scripts=[
        "scripts/caerp-split-pdf-run",
        "scripts/caerp-split-pdf-page2text",
        "scripts/caerp-change-code-analytic",
    ],
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest"],
    },
)
