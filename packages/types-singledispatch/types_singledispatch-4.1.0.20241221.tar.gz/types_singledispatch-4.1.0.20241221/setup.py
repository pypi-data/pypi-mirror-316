from setuptools import setup

name = "types-singledispatch"
description = "Typing stubs for singledispatch"
long_description = '''
## Typing stubs for singledispatch

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`singledispatch`](https://github.com/jaraco/singledispatch) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `singledispatch`. This version of
`types-singledispatch` aims to provide accurate annotations for
`singledispatch==4.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/singledispatch`](https://github.com/python/typeshed/tree/main/stubs/singledispatch)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`097581ea47d0fd77f097c88d80d5947e0218d9c4`](https://github.com/python/typeshed/commit/097581ea47d0fd77f097c88d80d5947e0218d9c4).
'''.lstrip()

setup(name=name,
      version="4.1.0.20241221",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/singledispatch.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['singledispatch-stubs'],
      package_data={'singledispatch-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
