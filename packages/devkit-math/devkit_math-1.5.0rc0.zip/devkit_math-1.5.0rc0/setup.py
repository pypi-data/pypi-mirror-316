from setuptools import setup, Extension
prime = Extension(
    name = "prime",
    sources = ["prime.cpp"],
    language = "c++"
)
setup(
    name = "devkit-math",
    version = "1.5.0c0",
    author = "Pemrilect",
    author_email = "retres243@outlook.com",
    license = "MIT",
    python_requires = ">=3.8",
    ext_modules = [prime],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)
