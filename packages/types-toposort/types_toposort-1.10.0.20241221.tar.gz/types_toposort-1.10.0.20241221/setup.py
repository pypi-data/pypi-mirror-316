from setuptools import setup

name = "types-toposort"
description = "Typing stubs for toposort"
long_description = '''
## Typing stubs for toposort

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`toposort`](https://gitlab.com/ericvsmith/toposort) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `toposort`. This version of
`types-toposort` aims to provide accurate annotations for
`toposort==1.10`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/toposort`](https://github.com/python/typeshed/tree/main/stubs/toposort)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`097581ea47d0fd77f097c88d80d5947e0218d9c4`](https://github.com/python/typeshed/commit/097581ea47d0fd77f097c88d80d5947e0218d9c4).
'''.lstrip()

setup(name=name,
      version="1.10.0.20241221",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/toposort.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['toposort-stubs'],
      package_data={'toposort-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
