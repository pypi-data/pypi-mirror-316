from setuptools import setup, find_packages

setup(
    name="MYLABLIBFORPYTHON",
    version="0.1.0",
    packages=find_packages(),
    description="Пример библиотеки с базовыми арифметическими операциями",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="moonbruh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
