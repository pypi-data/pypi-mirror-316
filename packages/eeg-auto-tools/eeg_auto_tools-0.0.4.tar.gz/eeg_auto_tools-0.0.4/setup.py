from setuptools import setup, find_packages
import pathlib

# Путь к текущей директории
here = pathlib.Path(__file__).parent.resolve()

# Чтение содержимого README.md
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="eeg_auto_tools",
    version="0.0.4",
    author="Sear",
    author_email="vasilijkrukovskij2015@gmail.com",
    description="The set of tools for working with EEG data",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
)