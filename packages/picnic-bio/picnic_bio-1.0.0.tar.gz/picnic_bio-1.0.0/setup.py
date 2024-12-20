import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = ""
    for line in fh:
        if line.startswith("# Development"):
            break
        long_description += line

setuptools.setup(
    name="picnic-bio",
    version="1.0.0",
    author="Anna Hadarovich <hadarovi@mpi-cbg.de>, Soumyadeep Ghosh <soumyadeep11194@gmail.com>, Maxim Scheremetjew <schereme@mpi-cbg.de>",
    author_email="picnic@cd-code.org",
    description="PICNIC (Proteins Involved in CoNdensates In Cells) is a machine learning-based model that predicts proteins involved in biomolecular condensates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://picnic.cd-code.org/",
    project_urls={
        "Documentation": "https://git.mpi-cbg.de/tothpetroczylab/picnic/-/blob/main/README.md",
        "Funding": "https://picnic.cd-code.org/about-us",
        "Source": "https://git.mpi-cbg.de/tothpetroczylab/picnic",
        "Tracker": "https://git.mpi-cbg.de/tothpetroczylab/picnic/-/issues",
    },
    keywords=["Biomolecular condensate", "Scientific Annotation Tool", "condensate", "machine learning"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    package_dir={"picnic_bio": "src"},
    package_data={"picnic_bio": ["files/models_llps/*", "files/iupred2a/data/*", "files/go/*"]},
    python_requires=">=3.9",
    install_requires=[
        "requests ~=2.32.0",
        "catboost ~=1.2.7",
        "matplotlib ~=3.9.4",
        "pandas ~=2.2.3",
        "Bio ~=1.6.2",
        "numpy ~=1.26.4",
    ],
    entry_points={
        "console_scripts": [
            "picnic = picnic_bio.main:main",
        ]
    },
)
