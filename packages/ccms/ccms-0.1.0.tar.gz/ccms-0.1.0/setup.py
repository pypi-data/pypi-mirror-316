from setuptools import setup, find_packages

setup(
    name="ccms",
    version="0.1.0",
    description="A Contract and Compliance Management System using Python and Supabase",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vinayak Rastogi",
    author_email="rvinayak108@gmail.com",
    url="https://github.com/VinVorteX/ccms",
    packages=find_packages(exclude=[
        '*.egg-info',
        '*.__pycache__',
        '*.__pycache__.*',
        '*.*.___pycache__',
        'tests',
        'tests.*'
    ]),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "PyPDF2",
        "rich",
        "python-docx",
        "supabase",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "ccms=ccms.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)