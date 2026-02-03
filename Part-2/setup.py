from setuptools import setup, find_packages

setup(
    name="Topsis-Tanish-102313008",
    version="1.0.0",
    author="Tanish Ahuja",
    author_email="tanishahuja06@gmail.com",
    description="Python package implementing TOPSIS method",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "openpyxl"],
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Tanish_102313008.topsis:main"
        ]
    },
)
