from setuptools import setup

name = "types-httplib2"
description = "Typing stubs for httplib2"
long_description = '''
## Typing stubs for httplib2

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`httplib2`](https://github.com/httplib2/httplib2) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `httplib2`. This version of
`types-httplib2` aims to provide accurate annotations for
`httplib2==0.22.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/httplib2`](https://github.com/python/typeshed/tree/main/stubs/httplib2)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`097581ea47d0fd77f097c88d80d5947e0218d9c4`](https://github.com/python/typeshed/commit/097581ea47d0fd77f097c88d80d5947e0218d9c4).
'''.lstrip()

setup(name=name,
      version="0.22.0.20241221",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/httplib2.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['httplib2-stubs'],
      package_data={'httplib2-stubs': ['__init__.pyi', 'auth.pyi', 'certs.pyi', 'error.pyi', 'iri2uri.pyi', 'socks.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
