from setuptools import setup, find_packages

setup(
    name="MyLabLibraryTAM1",
    version="0.1.2",
    test_suite='tests',
    author="Timur Mitrofanov",
    author_email="mitrofanov-t@bk.ru",
    description="Каастомная библиотека по второй лабораторной работе лог. програмирования",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MitrofanovTimurAlexsandrovich/my_library ",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
