from setuptools import setup, find_packages

setup(
    name='vitreous',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pillow>=11.0.0',
        'pytesseract>=0.3.13'
    ]
)
