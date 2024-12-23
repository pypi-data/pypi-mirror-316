from setuptools import setup, find_packages

setup(
    name="praktikum_nlp",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "ipython",
    ],
    extras_require={
        "ollamaUI": [],
        "ollamaUI_Vision": [],
    },
    author='Praktikum NLP',
    description='Library for Praktikum NLP UIR',
    long_description_content_type='text/plain',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)

