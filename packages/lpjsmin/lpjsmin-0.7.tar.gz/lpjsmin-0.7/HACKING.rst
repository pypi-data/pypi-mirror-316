Development setup
=================

To run this project's tests, use `tox <https://tox.readthedocs.io/en/latest/>`.

Release HOWTO
=============

To make a release,

  1) Update release date/version in NEWS.rst and setup.py
  2) Run 'python setup.py sdist'
  3) Test the generated source distribution in dist/
  4) Upload to PyPI: 'python setup.py sdist register upload'
  5) Increase version in setup.py (for next release)

