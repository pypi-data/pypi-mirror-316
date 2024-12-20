from setuptools import setup, find_packages

try:
    import flask
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

setup(
    name="FHeta",
    version="1.4.8.8",
    description="",
    author="FHeta",
    packages=find_packages(),
    install_requires=[
        "telethon",
        "requests",
    ] + (["flask"] if HAS_FLASK else []),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)